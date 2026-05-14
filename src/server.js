import fs from "node:fs";
import fsPromises from "node:fs/promises";
import path from "node:path";
import Fastify from "fastify";
import { chromium } from "playwright";
import { captureUrlScreenshot, ScreenshotError } from "./screenshot.js";
import { UrlValidationError } from "./security.js";

const DEFAULT_PORT = 3000;
const DEFAULT_HOST = "0.0.0.0";
const DEFAULT_OUTPUT_DIR = path.resolve(process.cwd(), "output/screenshots");
const IMAGE_TYPES = new Map([
  [".png", "image/png"],
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".webp", "image/webp"],
]);

export async function buildServer(options = {}) {
  const config = readServerConfig(options);
  const app = Fastify({
    logger: options.logger ?? true,
    bodyLimit: config.bodyLimit,
  });
  const limiter = createLimiter(config.maxConcurrency, config.maxQueueSize);
  const browser = options.browser ?? (await chromium.launch());
  const ownsBrowser = !options.browser;

  await fsPromises.mkdir(config.outputDir, { recursive: true });

  app.addHook("onClose", async () => {
    if (ownsBrowser) {
      await browser.close();
    }
  });

  app.get("/health", async () => ({
    ok: true,
    maxConcurrency: config.maxConcurrency,
    queueDepth: limiter.queueDepth(),
  }));

  app.post(
    "/screenshot",
    {
      schema: {
        body: {
          type: "object",
          required: ["url"],
          additionalProperties: false,
          properties: requestSchemaProperties(),
        },
      },
    },
    async (request, reply) => {
      const result = await runCapture(limiter, browser, config, request.body);
      reply.code(201);
      return withPublicUrl(result, request, config);
    },
  );

  app.get(
    "/screenshot",
    {
      schema: {
        querystring: {
          type: "object",
          required: ["url"],
          additionalProperties: false,
          properties: {
            ...requestSchemaProperties(),
            response: { type: "string", enum: ["image", "json"], default: "image" },
          },
        },
      },
    },
    async (request, reply) => {
      const result = await runCapture(limiter, browser, config, request.query);
      const publicResult = withPublicUrl(result, request, config);

      if (request.query.response === "json") {
        return publicResult;
      }

      const contentType = IMAGE_TYPES.get(path.extname(result.filePath).toLowerCase()) || "application/octet-stream";
      reply.type(contentType);
      reply.header("x-screenshot-url", result.url);
      reply.header("x-screenshot-width", String(result.width));
      reply.header("x-screenshot-height", String(result.height));
      return fs.createReadStream(result.filePath);
    },
  );

  app.get("/screenshots/:filename", async (request, reply) => {
    const filename = path.basename(request.params.filename);
    if (filename !== request.params.filename || !IMAGE_TYPES.has(path.extname(filename).toLowerCase())) {
      reply.code(404);
      return { error: "Not found" };
    }

    const filePath = path.resolve(config.outputDir, filename);
    if (!filePath.startsWith(config.outputDir + path.sep)) {
      reply.code(404);
      return { error: "Not found" };
    }

    try {
      await fsPromises.access(filePath);
    } catch {
      reply.code(404);
      return { error: "Not found" };
    }

    reply.type(IMAGE_TYPES.get(path.extname(filename).toLowerCase()));
    return fs.createReadStream(filePath);
  });

  app.setErrorHandler((error, request, reply) => {
    if (error instanceof UrlValidationError || error instanceof ScreenshotError) {
      reply.code(400).send({
        error: error.name,
        message: error.message,
        details: error.details || {},
      });
      return;
    }

    if (error.code === "QUEUE_FULL") {
      reply.code(503).send({
        error: "QueueFull",
        message: "Screenshot queue is full. Please retry later.",
      });
      return;
    }

    request.log.error(error);
    reply.code(500).send({
      error: "InternalServerError",
      message: "Failed to capture screenshot",
    });
  });

  return app;
}

async function runCapture(limiter, browser, config, requestOptions) {
  return limiter.run(() =>
    captureUrlScreenshot(requestOptions.url, {
      browser,
      outputDir: config.outputDir,
      width: requestOptions.width,
      height: requestOptions.height,
      deviceScaleFactor: requestOptions.deviceScaleFactor,
      format: requestOptions.format,
      quality: requestOptions.quality,
      timeoutMs: requestOptions.timeoutMs,
      waitAfterLoadMs: requestOptions.waitAfterLoadMs,
      maxPageHeight: requestOptions.maxPageHeight,
      tileHeight: requestOptions.tileHeight,
      maxScrolls: requestOptions.maxScrolls,
      allowPrivateNetwork: config.allowPrivateNetwork,
    }),
  );
}

function withPublicUrl(result, request, config) {
  const forwardedProto = request.headers["x-forwarded-proto"]?.split(",")[0]?.trim();
  const forwardedHost = request.headers["x-forwarded-host"]?.split(",")[0]?.trim();
  const protocol = forwardedProto || (request.raw.socket.encrypted ? "https" : "http");
  const host = forwardedHost || request.headers.host || "localhost";
  const baseUrl = config.publicBaseUrl || `${protocol}://${host}`;
  return {
    ...result,
    imageUrl: new URL(`/screenshots/${encodeURIComponent(result.filename)}`, baseUrl).toString(),
  };
}

function requestSchemaProperties() {
  return {
    url: { type: "string", minLength: 1, maxLength: 2048 },
    width: { type: "integer", minimum: 320, maximum: 7680, default: 1440 },
    height: { type: "integer", minimum: 320, maximum: 4320, default: 900 },
    deviceScaleFactor: { type: "number", minimum: 1, maximum: 3, default: 1 },
    format: { type: "string", enum: ["png", "jpeg", "webp"], default: "png" },
    quality: { type: "integer", minimum: 1, maximum: 100, default: 90 },
    timeoutMs: { type: "integer", minimum: 5000, maximum: 180000, default: 45000 },
    waitAfterLoadMs: { type: "integer", minimum: 0, maximum: 30000, default: 800 },
    maxPageHeight: { type: "integer", minimum: 1000, maximum: 100000, default: 50000 },
    tileHeight: { type: "integer", minimum: 1000, maximum: 50000, default: 8000 },
    maxScrolls: { type: "integer", minimum: 1, maximum: 500, default: 80 },
  };
}

function readServerConfig(options) {
  return {
    host: options.host ?? process.env.HOST ?? DEFAULT_HOST,
    port: Number(options.port ?? process.env.PORT ?? DEFAULT_PORT),
    outputDir: path.resolve(options.outputDir ?? process.env.SCREENSHOT_OUTPUT_DIR ?? DEFAULT_OUTPUT_DIR),
    publicBaseUrl: options.publicBaseUrl ?? process.env.PUBLIC_BASE_URL ?? "",
    maxConcurrency: Number(options.maxConcurrency ?? process.env.SCREENSHOT_MAX_CONCURRENCY ?? 2),
    maxQueueSize: Number(options.maxQueueSize ?? process.env.SCREENSHOT_MAX_QUEUE_SIZE ?? 20),
    bodyLimit: Number(options.bodyLimit ?? process.env.SCREENSHOT_BODY_LIMIT ?? 32 * 1024),
    allowPrivateNetwork: options.allowPrivateNetwork ?? process.env.ALLOW_PRIVATE_URLS === "1",
  };
}

function createLimiter(maxConcurrency, maxQueueSize) {
  let active = 0;
  const queue = [];

  return {
    queueDepth: () => queue.length,
    async run(task) {
      if (active < maxConcurrency) {
        active += 1;
      } else {
        if (queue.length >= maxQueueSize) {
          const error = new Error("Queue is full");
          error.code = "QUEUE_FULL";
          throw error;
        }

        await new Promise((resolve) => queue.push(resolve));
      }

      try {
        return await task();
      } finally {
        active -= 1;
        const next = queue.shift();
        if (next) {
          active += 1;
          next();
        }
      }
    },
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const server = await buildServer();
  const config = readServerConfig({});

  try {
    await server.listen({ host: config.host, port: config.port });
  } catch (error) {
    server.log.error(error);
    process.exit(1);
  }
}
