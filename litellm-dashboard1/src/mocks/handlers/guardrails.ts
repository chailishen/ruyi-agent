import { http } from "msw";
import guardrailsList from "@/mocks/fixtures/guardrails-list.json";
import { jsonResponse } from "@/mocks/utils";

export const guardrailsHandlers = [
  http.get("*/v2/guardrails/list", () => jsonResponse(guardrailsList)),
  http.get("*/guardrails/list", () => jsonResponse(guardrailsList)),
  http.get("*/guardrails/submissions", () => jsonResponse({ submissions: [] })),
  http.get("*/guardrails/usage/overview", () =>
    jsonResponse({
      guardrails: guardrailsList.guardrails.map((g) => ({
        guardrail_id: g.guardrail_id,
        guardrail_name: g.guardrail_name,
        total_requests: 120,
        blocked_requests: 3,
      })),
    }),
  ),
  http.get("*/guardrails/usage/detail/*", () =>
    jsonResponse({ daily_data: [], total_requests: 120, blocked_requests: 3 }),
  ),
  http.get("*/guardrails/usage/logs", () => jsonResponse({ logs: [], total: 0 })),
  http.post("*/guardrails", () => jsonResponse({ guardrail_id: `gr-${Date.now()}` })),
];
