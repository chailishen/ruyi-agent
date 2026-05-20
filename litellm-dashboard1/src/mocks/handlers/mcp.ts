import { http } from "msw";
import mcpServers from "@/mocks/fixtures/mcp-servers.json";
import { jsonResponse } from "@/mocks/utils";

const healthPayload = Object.fromEntries(
  mcpServers.map((s) => [s.server_id, { status: "healthy", latency_ms: 42 }]),
);

export const mcpHandlers = [
  http.get("*/v1/mcp/server", () => jsonResponse(mcpServers)),
  http.get("*/v1/mcp/server/health", () => jsonResponse(healthPayload)),
  http.get("*/v1/mcp/access_groups", () => jsonResponse([])),
  http.get("*/v1/mcp/toolset", () => jsonResponse([])),
  http.get("*/v1/mcp/server/submissions", () => jsonResponse([])),
  http.post("*/v1/mcp/server", () => jsonResponse({ server_id: `mcp-${Date.now()}` })),
  http.patch("*/v1/mcp/server/*", () => jsonResponse({ status: "ok" })),
  http.delete("*/v1/mcp/server/*", () => jsonResponse({ status: "ok" })),
  http.post("*/v1/mcp/server/register", () => jsonResponse({ server_id: `mcp-${Date.now()}` })),
  http.get("*/mcp-rest/tools/list", () => jsonResponse({ tools: [] })),
  http.post("*/mcp-rest/tools/call", () => jsonResponse({ result: "mock tool output" })),
  http.post("*/v1/mcp/server/oauth/session", () => jsonResponse({ authorization_url: null })),
];
