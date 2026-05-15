#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";
import { captureUrlScreenshot, ScreenshotError } from "./screenshot.js";
import { UrlValidationError } from "./security.js";

const COMMON_OPTION_KEYS = new Set([
  "outputDir",
  "width",
  "height",
  "deviceScaleFactor",
  "format",
  "quality",
  "timeoutMs",
  "waitAfterLoadMs",
  "maxPageHeight",
  "tileHeight",
  "maxScrolls",
  "allowPrivateNetwork",
]);

try {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const batch = await loadBatch(args);
  const result = await runBatch(batch);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.failures.length > 0 ? 1 : 0);
} catch (error) {
  if (error instanceof UrlValidationError || error instanceof ScreenshotError) {
    console.error(`${error.name}: ${error.message}`);
    if (Object.keys(error.details || {}).length > 0) {
      console.error(JSON.stringify(error.details, null, 2));
    }
    process.exit(2);
  }

  console.error(error);
  process.exit(1);
}

async function loadBatch(args) {
  const fileConfig = args.input ? await readJson(args.input) : {};
  const inlineTargets = args.targets.length > 0 ? args.targets : undefined;
  const targets = inlineTargets ?? fileConfig.items ?? fileConfig.targets ?? [];
  const options = {
    ...pickCommonOptions(fileConfig),
    ...pickCommonOptions(args),
  };

  if (targets.length === 0) {
    throw new ScreenshotError("No batch items provided. Use --input=<file> or --target=<name>=<url>.");
  }

  return {
    options,
    items: normalizeItems(targets),
  };
}

async function readJson(filePath) {
  const content = await fs.readFile(path.resolve(filePath), "utf8");
  return JSON.parse(content);
}

async function runBatch(batch) {
  const browser = await chromium.launch();
  const successes = [];
  const failures = [];

  try {
    for (const item of batch.items) {
      const outputFile = resolveNamedOutputFile(item.name, batch.options);

      try {
        const result = await captureUrlScreenshot(item.url, {
          ...batch.options,
          outputFile,
          browser,
        });

        successes.push({
          name: item.name,
          ...result,
        });
      } catch (error) {
        failures.push({
          name: item.name,
          url: item.url,
          error: error.message,
          details: error.details ?? {},
        });
      }
    }
  } finally {
    await browser.close();
  }

  return {
    total: batch.items.length,
    successCount: successes.length,
    failureCount: failures.length,
    successes,
    failures,
  };
}

function normalizeItems(items) {
  if (!Array.isArray(items)) {
    throw new ScreenshotError("Batch items must be an array");
  }

  return items.map((item, index) => {
    if (!item || typeof item !== "object") {
      throw new ScreenshotError(`Batch item at index ${index} must be an object`);
    }

    const name = String(item.name ?? "").trim();
    const url = String(item.url ?? "").trim();

    if (!name) {
      throw new ScreenshotError(`Batch item at index ${index} is missing name`);
    }

    if (!url) {
      throw new ScreenshotError(`Batch item "${name}" is missing url`);
    }

    return { name, url };
  });
}

function resolveNamedOutputFile(name, options) {
  const outputDir = path.resolve(String(options.outputDir ?? "output/screenshots"));
  const format = String(options.format ?? "png").toLowerCase();
  const filename = `${sanitizeFilename(name)}.${extensionFor(format)}`;
  return path.join(outputDir, filename);
}

function pickCommonOptions(value) {
  return Object.fromEntries(
    Object.entries(value).filter(([key, entry]) => COMMON_OPTION_KEYS.has(key) && entry !== undefined),
  );
}

function parseArgs(argv) {
  const parsed = {
    targets: [],
  };

  for (const arg of argv) {
    if (arg === "--help" || arg === "-h") {
      parsed.help = true;
      continue;
    }

    if (!arg.startsWith("--") && !parsed.input) {
      parsed.input = arg;
      continue;
    }

    if (!arg.startsWith("--")) {
      continue;
    }

    const [rawKey, ...rawValueParts] = arg.slice(2).split("=");
    const rawValue = rawValueParts.length > 0 ? rawValueParts.join("=") : "true";
    const key = toCamelCase(rawKey);

    if (key === "target") {
      parsed.targets.push(parseTarget(rawValue));
      continue;
    }

    parsed[key] = coerceValue(key, rawValue);
  }

  return parsed;
}

function parseTarget(value) {
  const separatorIndex = value.indexOf("=");

  if (separatorIndex <= 0) {
    throw new ScreenshotError("--target must use <name>=<url>");
  }

  return {
    name: value.slice(0, separatorIndex),
    url: value.slice(separatorIndex + 1),
  };
}

function coerceValue(key, value) {
  if (["allowPrivateNetwork"].includes(key)) {
    return value === "true" || value === "1";
  }

  if (
    [
      "width",
      "height",
      "deviceScaleFactor",
      "quality",
      "timeoutMs",
      "waitAfterLoadMs",
      "maxPageHeight",
      "tileHeight",
      "maxScrolls",
    ].includes(key)
  ) {
    return Number(value);
  }

  return value;
}

function toCamelCase(value) {
  return value.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
}

function sanitizeFilename(value) {
  return value.replace(/[\/\\:*?"<>|]+/g, "-").replace(/^-+|-+$/g, "").trim() || "screenshot";
}

function extensionFor(format) {
  return format === "jpeg" ? "jpg" : format;
}

function printHelp() {
  console.log(`Usage:
  npm run screenshot:batch -- --input=batch-screenshots.example.json
  npm run screenshot:batch -- --output-dir=output/batch --target=home=https://xailab.com.cn/ --target=docs=https://example.com/

Batch JSON:
  {
    "outputDir": "output/batch",
    "width": 1440,
    "height": 900,
    "format": "png",
    "maxPageHeight": 50000,
    "tileHeight": 8000,
    "items": [
      { "name": "home", "url": "https://xailab.com.cn/" }
    ]
  }

Options:
  --input=<file>               Batch JSON file
  --target=<name>=<url>        Add one target, can be repeated
  --output-dir=<dir>           Output directory, defaults to output/screenshots
  --width=<px>                 Viewport width, defaults to 1440
  --height=<px>                Viewport height, defaults to 900
  --format=<png|jpeg|webp>     Output format, defaults to png
  --quality=<1-100>            jpeg/webp quality, defaults to 90
  --timeout-ms=<ms>            Navigation timeout, defaults to 45000
  --max-page-height=<px>       Abort pages above this height, defaults to 50000
  --tile-height=<px>           Long-page tile height, defaults to 8000
  --allow-private-network=true Allow localhost/private IPs for local development
`);
}
