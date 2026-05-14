import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";
import sharp from "sharp";
import { createUrlGuard, validatePublicHttpUrl } from "./security.js";

export const DEFAULT_SCREENSHOT_OPTIONS = {
  outputDir: path.resolve(process.cwd(), "output/screenshots"),
  width: 1440,
  height: 900,
  deviceScaleFactor: 1,
  format: "png",
  quality: 90,
  timeoutMs: 45000,
  waitAfterLoadMs: 800,
  scrollDelayMs: 160,
  maxScrolls: 80,
  maxPageHeight: 50000,
  tileHeight: 8000,
  userAgent: "",
  allowPrivateNetwork: process.env.ALLOW_PRIVATE_URLS === "1",
};

const SUPPORTED_FORMATS = new Set(["png", "jpeg", "webp"]);
const NETWORK_IDLE_TIMEOUT_MS = 15000;
const IMAGE_WAIT_TIMEOUT_MS = 5000;

export class ScreenshotError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = "ScreenshotError";
    this.details = details;
  }
}

export async function captureUrlScreenshot(inputUrl, options = {}) {
  const config = normalizeOptions(options);
  const url = await validatePublicHttpUrl(inputUrl, {
    allowPrivateNetwork: config.allowPrivateNetwork,
  });

  await fs.mkdir(config.outputDir, { recursive: true });

  const browser = options.browser ?? (await chromium.launch());
  const ownsBrowser = !options.browser;

  try {
    const context = await browser.newContext({
      viewport: { width: config.width, height: config.height },
      deviceScaleFactor: config.deviceScaleFactor,
      locale: "zh-CN",
      reducedMotion: "reduce",
      userAgent: config.userAgent || undefined,
    });

    try {
      const page = await context.newPage();
      page.setDefaultTimeout(config.timeoutMs);
      page.setDefaultNavigationTimeout(config.timeoutMs);
      await installRequestGuard(page, config);
      await disableAnimations(page);

      await page.goto(url.toString(), {
        waitUntil: "domcontentloaded",
        timeout: config.timeoutMs,
      });

      await waitForStablePage(page, config);
      await triggerLazyLoading(page, config);
      await waitForStablePage(page, config);
      await expandPrimaryScrollContainer(page);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(200);

      const pageSize = await getPageSize(page, config.maxPageHeight);
      const filePath = resolveOutputPath(url, config);
      const usedTiling = pageSize.height > config.tileHeight;

      if (usedTiling) {
        await captureTiledScreenshot(page, filePath, pageSize, config);
      } else {
        await page.screenshot({
          path: filePath,
          fullPage: true,
          type: config.format,
          quality: qualityFor(config),
          scale: "css",
          animations: "disabled",
          caret: "hide",
        });
      }

      return {
        url: url.toString(),
        filePath,
        filename: path.basename(filePath),
        format: config.format,
        width: pageSize.width,
        height: pageSize.height,
        usedTiling,
      };
    } finally {
      await context.close();
    }
  } finally {
    if (ownsBrowser) {
      await browser.close();
    }
  }
}

export function normalizeOptions(options = {}) {
  const merged = {
    ...DEFAULT_SCREENSHOT_OPTIONS,
    ...dropUndefined(options),
  };

  const width = toInteger(merged.width, "width");
  const height = toInteger(merged.height, "height");
  const deviceScaleFactor = Number(merged.deviceScaleFactor);
  const maxPageHeight = toInteger(merged.maxPageHeight, "maxPageHeight");
  const tileHeight = toInteger(merged.tileHeight, "tileHeight");
  const timeoutMs = toInteger(merged.timeoutMs, "timeoutMs");
  const waitAfterLoadMs = toInteger(merged.waitAfterLoadMs, "waitAfterLoadMs");
  const scrollDelayMs = toInteger(merged.scrollDelayMs, "scrollDelayMs");
  const maxScrolls = toInteger(merged.maxScrolls, "maxScrolls");
  const format = String(merged.format).toLowerCase();

  if (width < 320 || width > 7680) {
    throw new ScreenshotError("width must be between 320 and 7680");
  }

  if (height < 320 || height > 4320) {
    throw new ScreenshotError("height must be between 320 and 4320");
  }

  if (!Number.isFinite(deviceScaleFactor) || deviceScaleFactor < 1 || deviceScaleFactor > 3) {
    throw new ScreenshotError("deviceScaleFactor must be between 1 and 3");
  }

  if (!SUPPORTED_FORMATS.has(format)) {
    throw new ScreenshotError(`format must be one of: ${[...SUPPORTED_FORMATS].join(", ")}`);
  }

  if (maxPageHeight < height || maxPageHeight > 100000) {
    throw new ScreenshotError("maxPageHeight must be between viewport height and 100000");
  }

  if (tileHeight < 1000 || tileHeight > maxPageHeight) {
    throw new ScreenshotError("tileHeight must be between 1000 and maxPageHeight");
  }

  if (timeoutMs < 5000 || timeoutMs > 180000) {
    throw new ScreenshotError("timeoutMs must be between 5000 and 180000");
  }

  return {
    ...merged,
    width,
    height,
    deviceScaleFactor,
    maxPageHeight,
    tileHeight,
    timeoutMs,
    waitAfterLoadMs,
    scrollDelayMs,
    maxScrolls,
    format,
    outputDir: path.resolve(String(merged.outputDir)),
  };
}

async function installRequestGuard(page, config) {
  if (config.allowPrivateNetwork) {
    return;
  }

  const guardUrl = await createUrlGuard({
    allowPrivateNetwork: config.allowPrivateNetwork,
  });

  await page.route("**/*", async (route) => {
    const requestUrl = route.request().url();
    const protocol = new URL(requestUrl).protocol;

    if (!["http:", "https:"].includes(protocol)) {
      await route.continue();
      return;
    }

    try {
      await guardUrl(requestUrl);
      await route.continue();
    } catch {
      await route.abort("blockedbyclient");
    }
  });
}

async function disableAnimations(page) {
  await page.addInitScript(() => {
    const style = document.createElement("style");
    style.textContent = `
      *,
      *::before,
      *::after {
        animation-duration: 0.001s !important;
        animation-delay: 0s !important;
        transition-duration: 0.001s !important;
        transition-delay: 0s !important;
        scroll-behavior: auto !important;
      }
    `;
    document.documentElement.appendChild(style);
  });
}

async function waitForStablePage(page, config) {
  await page.waitForLoadState("domcontentloaded");
  await page.waitForLoadState("networkidle", { timeout: NETWORK_IDLE_TIMEOUT_MS }).catch(() => {});
  await page.waitForTimeout(config.waitAfterLoadMs);

  await page.evaluate(async (imageWaitTimeoutMs) => {
    await document.fonts?.ready?.catch?.(() => {});
    const images = [...document.images].filter((image) => !image.complete);
    await Promise.race([
      Promise.allSettled(
        images.map(
          (image) =>
            new Promise((resolve) => {
              image.addEventListener("load", resolve, { once: true });
              image.addEventListener("error", resolve, { once: true });
            }),
        ),
      ),
      new Promise((resolve) => setTimeout(resolve, imageWaitTimeoutMs)),
    ]);
  }, IMAGE_WAIT_TIMEOUT_MS);
}

async function triggerLazyLoading(page, config) {
  await page.evaluate(
    async ({ maxScrolls, scrollDelayMs, maxPageHeight }) => {
      const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      const scroller = findPrimaryScroller();
      const isWindowScroller =
        scroller === document.scrollingElement || scroller === document.documentElement || scroller === document.body;
      const getScrollHeight = () =>
        isWindowScroller
          ? document.scrollingElement?.scrollHeight || document.body.scrollHeight
          : scroller.scrollHeight;
      const getViewportHeight = () => (isWindowScroller ? window.innerHeight : scroller.clientHeight);
      const scrollToY = (y) => {
        if (isWindowScroller) {
          window.scrollTo(0, y);
        } else {
          scroller.scrollTo(0, y);
        }
      };
      let previousHeight = 0;
      let stableCount = 0;

      for (let count = 0; count < maxScrolls; count += 1) {
        const scrollHeight = Math.min(getScrollHeight(), maxPageHeight);
        const y = Math.min(count * Math.max(getViewportHeight() * 0.75, 500), scrollHeight);

        scrollToY(y);
        await sleep(scrollDelayMs);

        if (scrollHeight === previousHeight) {
          stableCount += 1;
        } else {
          stableCount = 0;
          previousHeight = scrollHeight;
        }

        if (y + getViewportHeight() >= scrollHeight && stableCount >= 2) {
          break;
        }
      }

      scrollToY(0);
      await sleep(200);

      function findPrimaryScroller() {
        const documentScroller = document.scrollingElement || document.documentElement;
        if (documentScroller.scrollHeight > documentScroller.clientHeight + 50) {
          return documentScroller;
        }

        const candidates = [...document.querySelectorAll("body *")]
          .filter((element) => {
            const style = getComputedStyle(element);
            const overflowY = style.overflowY;
            const rect = element.getBoundingClientRect();
            return (
              ["auto", "scroll", "overlay"].includes(overflowY) &&
              element.scrollHeight > element.clientHeight + 50 &&
              rect.width >= window.innerWidth * 0.5 &&
              rect.height >= window.innerHeight * 0.5
            );
          })
          .sort((a, b) => b.scrollHeight - a.scrollHeight);

        return candidates[0] || documentScroller;
      }
    },
    {
      maxScrolls: config.maxScrolls,
      scrollDelayMs: config.scrollDelayMs,
      maxPageHeight: config.maxPageHeight,
    },
  );
}

async function expandPrimaryScrollContainer(page) {
  await page.evaluate(() => {
    const documentScroller = document.scrollingElement || document.documentElement;
    if (documentScroller.scrollHeight > documentScroller.clientHeight + 50) {
      return;
    }

    const candidates = [...document.querySelectorAll("body *")]
      .filter((element) => {
        const style = getComputedStyle(element);
        const overflowY = style.overflowY;
        const rect = element.getBoundingClientRect();
        return (
          ["auto", "scroll", "overlay"].includes(overflowY) &&
          element.scrollHeight > element.clientHeight + 50 &&
          rect.width >= window.innerWidth * 0.5 &&
          rect.height >= window.innerHeight * 0.5
        );
      })
      .sort((a, b) => b.scrollHeight - a.scrollHeight);

    const primaryScroller = candidates[0];
    if (!primaryScroller) {
      return;
    }

    const fullHeight = primaryScroller.scrollHeight;
    const fullWidth = Math.max(primaryScroller.scrollWidth, primaryScroller.clientWidth);

    document.documentElement.style.setProperty("height", "auto", "important");
    document.documentElement.style.setProperty("min-height", `${fullHeight}px`, "important");
    document.documentElement.style.setProperty("overflow", "visible", "important");
    document.body.style.setProperty("height", "auto", "important");
    document.body.style.setProperty("min-height", `${fullHeight}px`, "important");
    document.body.style.setProperty("overflow", "visible", "important");

    primaryScroller.scrollTo(0, 0);
    primaryScroller.style.setProperty("height", `${fullHeight}px`, "important");
    primaryScroller.style.setProperty("min-height", `${fullHeight}px`, "important");
    primaryScroller.style.setProperty("width", `${fullWidth}px`, "important");
    primaryScroller.style.setProperty("overflow", "visible", "important");
    primaryScroller.style.setProperty("max-height", "none", "important");
  });
}

async function getPageSize(page, maxPageHeight) {
  const size = await page.evaluate(() => {
    const scrollingElement = document.scrollingElement || document.documentElement;
    const body = document.body;
    const width = Math.ceil(
      Math.max(
        scrollingElement.scrollWidth,
        scrollingElement.clientWidth,
        body?.scrollWidth || 0,
        body?.offsetWidth || 0,
      ),
    );
    const height = Math.ceil(
      Math.max(
        scrollingElement.scrollHeight,
        scrollingElement.clientHeight,
        body?.scrollHeight || 0,
        body?.offsetHeight || 0,
      ),
    );

    return { width, height };
  });

  if (size.height > maxPageHeight) {
    throw new ScreenshotError("Page exceeds maxPageHeight", {
      pageHeight: size.height,
      maxPageHeight,
    });
  }

  return size;
}

async function captureTiledScreenshot(page, filePath, pageSize, config) {
  const inputs = [];
  const originalViewport = page.viewportSize();

  try {
    for (let y = 0; y < pageSize.height; y += config.tileHeight) {
      const height = Math.min(config.tileHeight, pageSize.height - y);
      await page.setViewportSize({
        width: pageSize.width,
        height,
      });
      await page.evaluate((scrollY) => window.scrollTo(0, scrollY), y);
      await page.waitForTimeout(80);

      const buffer = await page.screenshot({
        type: "png",
        scale: "css",
        animations: "disabled",
        caret: "hide",
      });

      inputs.push({
        input: buffer,
        top: y,
        left: 0,
      });
    }
  } finally {
    if (originalViewport) {
      await page.setViewportSize(originalViewport);
    }
  }

  let image = sharp({
    create: {
      width: pageSize.width,
      height: pageSize.height,
      channels: 4,
      background: { r: 255, g: 255, b: 255, alpha: 0 },
    },
  }).composite(inputs);

  if (config.format === "jpeg") {
    image = image.jpeg({ quality: config.quality, mozjpeg: true });
  } else if (config.format === "webp") {
    image = image.webp({ quality: config.quality });
  } else {
    image = image.png();
  }

  await image.toFile(filePath);
}

function resolveOutputPath(url, config) {
  if (config.outputFile) {
    return path.resolve(String(config.outputFile));
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const name = `${sanitizeFilename(url.hostname)}-${timestamp}.${extensionFor(config.format)}`;
  return path.resolve(config.outputDir, name);
}

function sanitizeFilename(value) {
  return value.replace(/[^a-zA-Z0-9.-]+/g, "-").replace(/^-+|-+$/g, "") || "screenshot";
}

function extensionFor(format) {
  return format === "jpeg" ? "jpg" : format;
}

function qualityFor(config) {
  return config.format === "png" ? undefined : config.quality;
}

function toInteger(value, name) {
  const number = Number(value);
  if (!Number.isInteger(number)) {
    throw new ScreenshotError(`${name} must be an integer`);
  }
  return number;
}

function dropUndefined(value) {
  return Object.fromEntries(Object.entries(value).filter(([, entry]) => entry !== undefined));
}
