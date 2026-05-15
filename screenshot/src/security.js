import dns from "node:dns/promises";
import net from "node:net";

const DEFAULT_BLOCKED_HOSTS = new Set([
  "0.0.0.0",
  "127.0.0.1",
  "localhost",
  "metadata.google.internal",
]);

const CLOUD_METADATA_IPV4 = "169.254.169.254";

export class UrlValidationError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = "UrlValidationError";
    this.details = details;
  }
}

export function normalizeHttpUrl(input) {
  let url;
  try {
    url = new URL(input);
  } catch {
    throw new UrlValidationError("Invalid URL");
  }

  if (!["http:", "https:"].includes(url.protocol)) {
    throw new UrlValidationError("Only http and https URLs are supported", {
      protocol: url.protocol,
    });
  }

  if (url.username || url.password) {
    throw new UrlValidationError("URLs with embedded credentials are not supported");
  }

  return url;
}

export async function validatePublicHttpUrl(input, options = {}) {
  const {
    allowPrivateNetwork = false,
    maxUrlLength = 2048,
    dnsLookup = dns.lookup,
  } = options;

  if (typeof input !== "string" || input.trim().length === 0) {
    throw new UrlValidationError("URL is required");
  }

  if (input.length > maxUrlLength) {
    throw new UrlValidationError("URL is too long", { maxUrlLength });
  }

  const url = normalizeHttpUrl(input.trim());
  const hostname = normalizeHostname(url.hostname);

  if (!allowPrivateNetwork) {
    if (DEFAULT_BLOCKED_HOSTS.has(hostname) || hostname.endsWith(".localhost")) {
      throw new UrlValidationError("Private or local hosts are not allowed", {
        hostname,
      });
    }

    if (net.isIP(hostname)) {
      assertPublicIp(hostname);
    } else {
      let records;
      try {
        records = await dnsLookup(hostname, { all: true, verbatim: true });
      } catch (error) {
        throw new UrlValidationError("Unable to resolve URL hostname", {
          hostname,
          cause: error.message,
        });
      }

      if (records.length === 0) {
        throw new UrlValidationError("Hostname did not resolve to any address", {
          hostname,
        });
      }

      for (const record of records) {
        assertPublicIp(record.address);
      }
    }
  }

  return url;
}

export async function createUrlGuard(options = {}) {
  const cache = new Map();

  return async function guardUrl(input) {
    const url = normalizeHttpUrl(input);
    const hostname = normalizeHostname(url.hostname);
    const cacheKey = `${url.protocol}//${hostname}:${url.port || ""}`;

    if (!cache.has(cacheKey)) {
      const validation = validatePublicHttpUrl(url.toString(), options).catch((error) => {
        cache.delete(cacheKey);
        throw error;
      });
      cache.set(cacheKey, validation);
    }

    await cache.get(cacheKey);
    return url;
  };
}

function assertPublicIp(address) {
  if (isPrivateOrReservedIp(address)) {
    throw new UrlValidationError("Private, local, or reserved IP addresses are not allowed", {
      address,
    });
  }
}

function normalizeHostname(hostname) {
  return hostname.toLowerCase().replace(/^\[|\]$/g, "");
}

export function isPrivateOrReservedIp(address) {
  const version = net.isIP(address);

  if (version === 4) {
    return isPrivateOrReservedIpv4(address);
  }

  if (version === 6) {
    return isPrivateOrReservedIpv6(address);
  }

  return true;
}

function isPrivateOrReservedIpv4(address) {
  if (address === CLOUD_METADATA_IPV4) {
    return true;
  }

  const parts = address.split(".").map((part) => Number(part));
  if (parts.length !== 4 || parts.some((part) => Number.isNaN(part) || part < 0 || part > 255)) {
    return true;
  }

  const [a, b] = parts;

  return (
    a === 0 ||
    a === 10 ||
    a === 127 ||
    (a === 100 && b >= 64 && b <= 127) ||
    (a === 169 && b === 254) ||
    (a === 172 && b >= 16 && b <= 31) ||
    (a === 192 && b === 0) ||
    (a === 192 && b === 168) ||
    (a === 198 && (b === 18 || b === 19)) ||
    a >= 224
  );
}

function isPrivateOrReservedIpv6(address) {
  const normalized = address.toLowerCase();

  return (
    normalized === "::" ||
    normalized === "::1" ||
    normalized.startsWith("fc") ||
    normalized.startsWith("fd") ||
    normalized.startsWith("fe8") ||
    normalized.startsWith("fe9") ||
    normalized.startsWith("fea") ||
    normalized.startsWith("feb") ||
    normalized.startsWith("ff") ||
    normalized.startsWith("2001:db8")
  );
}
