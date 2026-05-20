import { http } from "msw";
import modelHub from "@/mocks/fixtures/model-hub-public.json";
import { jsonResponse } from "@/mocks/utils";

export const hubPublicHandlers = [
  http.get("*/public/model_hub", () => jsonResponse(modelHub)),
  http.get("*/public/model_hub/info", () => jsonResponse({ model_groups: modelHub })),
  http.get("*/model_hub", () => jsonResponse(modelHub)),
  http.get("*/public/agent_hub", () => jsonResponse([])),
  http.get("*/public/mcp_hub", () => jsonResponse([])),
];
