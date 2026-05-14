#!/usr/bin/env node
import { captureUrlScreenshot, ScreenshotError } from "./screenshot.js";
import { UrlValidationError } from "./security.js";

const args = parseArgs(process.argv.slice(2));

if (args.help || !args.url) {
  printHelp();
  process.exit(args.help ? 0 : 1);
}

try {
  const result = await captureUrlScreenshot(args.url, {
    outputFile: args.output,
    outputDir: args.outputDir,
    width: args.width,
    height: args.height,
    deviceScaleFactor: args.deviceScaleFactor,
    format: args.format,
    quality: args.quality,
    timeoutMs: args.timeoutMs,
    waitAfterLoadMs: args.waitAfterLoadMs,
    maxPageHeight: args.maxPageHeight,
    tileHeight: args.tileHeight,
    maxScrolls: args.maxScrolls,
    allowPrivateNetwork: args.allowPrivateNetwork,
  });

  console.log(JSON.stringify(result, null, 2));
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

function parseArgs(argv) {
  const parsed = {};

  for (const arg of argv) {
    if (arg === "--help" || arg === "-h") {
      parsed.help = true;
      continue;
    }

    if (!arg.startsWith("--") && !parsed.url) {
      parsed.url = arg;
      continue;
    }

    if (!arg.startsWith("--")) {
      continue;
    }

    const [rawKey, rawValue = "true"] = arg.slice(2).split("=");
    const key = toCamelCase(rawKey);
    parsed[key] = coerceValue(key, rawValue);
  }

  return parsed;
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

function printHelp() {
  console.log(`Usage:
  npm run screenshot -- <url> [options]

Examples:
  npm run screenshot -- https://xailab.com.cn/
  npm run screenshot -- https://xailab.com.cn/ --output=output/xailab.png --width=1440 --height=900

Options:
  --output=<file>              Write to a specific file
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
