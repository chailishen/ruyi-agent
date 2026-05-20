import { delay, HttpResponse } from "msw";
import { mockLatency } from "@/mocks/config";

export async function jsonResponse(
  data: unknown,
  init?: { status?: number; delayMs?: number },
) {
  const wait = init?.delayMs ?? mockLatency();
  await delay(wait);
  return HttpResponse.json(data as Record<string, unknown>, { status: init?.status ?? 200 });
}

export function parseBearer(request: Request): string | null {
  const auth = request.headers.get("Authorization") ?? request.headers.get("authorization");
  if (!auth?.startsWith("Bearer ")) return null;
  return auth.slice(7);
}

export function requireAuth(request: Request): boolean {
  return parseBearer(request) !== null;
}
