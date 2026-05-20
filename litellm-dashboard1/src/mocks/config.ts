export const isMockMode = (): boolean =>
  typeof process !== "undefined" && process.env.NEXT_PUBLIC_MOCK_MODE === "true";

export const mockLatency = (): number => {
  const min = Number(process.env.NEXT_PUBLIC_MOCK_LATENCY_MS_MIN ?? 200);
  const max = Number(process.env.NEXT_PUBLIC_MOCK_LATENCY_MS_MAX ?? 600);
  return min + Math.random() * (max - min);
};

export const mockDefaultRole = (): string =>
  process.env.NEXT_PUBLIC_MOCK_DEFAULT_ROLE ?? "proxy_admin";
