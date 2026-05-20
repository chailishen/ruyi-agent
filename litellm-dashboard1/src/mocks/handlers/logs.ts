import { http } from "msw";
import spendLogs from "@/mocks/fixtures/spend-logs.json";
import { jsonResponse } from "@/mocks/utils";

export const logsHandlers = [
  http.get("*/spend/logs/ui", () => jsonResponse(spendLogs)),
];
