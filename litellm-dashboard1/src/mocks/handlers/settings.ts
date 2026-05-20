import { http } from "msw";
import { jsonResponse } from "@/mocks/utils";

export const settingsHandlers = [
  http.get("*/alerting/settings", () => jsonResponse({ settings: {} })),
  http.get("*/callbacks/configs", () => jsonResponse([])),
  http.get("*/config/list", () => jsonResponse({ configs: [] })),
  http.post("*/config/update", () => jsonResponse({ status: "ok" })),
  http.get("*/get/allowed_ips", () => jsonResponse({ allowed_ips: [] })),
  http.get("*/allowed_ips", () => jsonResponse({ allowed_ips: [] })),
];
