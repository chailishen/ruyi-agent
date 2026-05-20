import { http } from "msw";
import modelsAvailable from "@/mocks/fixtures/models-available.json";
import { jsonResponse } from "@/mocks/utils";

export const commonHandlers = [
  http.get("*/user/available_roles", () =>
    jsonResponse({ roles: ["proxy_admin", "proxy_admin_viewer", "internal_user"] }),
  ),
  http.get("*/v2/model/info", () =>
    jsonResponse({
      data: [
        {
          model_name: "gpt-4o",
          litellm_params: { model: "openai/gpt-4o", api_key: "mock" },
          model_info: { id: "model-001", mode: "chat" },
        },
      ],
    }),
  ),
  http.get("*/model_group/info", () => jsonResponse({ data: [] })),
  http.get("*/public/litellm_model_cost_map", () => jsonResponse({})),
  http.get("*/public/providers/fields", () => jsonResponse({ providers: [] })),
  http.get("*/public/agents/fields", () => jsonResponse({ fields: [] })),
  http.get("*/credentials", () => jsonResponse([])),
  http.get("*/team/available", () => jsonResponse([])),
  http.get("*/customer/list", () => jsonResponse([])),
  http.get("*/global/spend/keys", () => jsonResponse([])),
  http.get("*/global/spend/models", () => jsonResponse([])),
  http.get("*/global/spend/end_users", () => jsonResponse([])),
  http.get("*/global/spend/provider", () => jsonResponse([])),
  http.get("*/global/spend/tags", () => jsonResponse({ spend_per_tag: [] })),
  http.get("*/global/spend/all_tag_names", () => jsonResponse([])),
  http.get("*/policies/list", () => jsonResponse({ policies: [] })),
  http.get("*/v2/policies/list", () => jsonResponse({ policies: [] })),
  http.get("*/agent/list", () => jsonResponse({ agents: [] })),
  http.get("*/v1/agents", () => jsonResponse({ agents: [] })),
  http.get("*/budget/list", () => jsonResponse([])),
  http.get("*/blog/posts", () => jsonResponse({ posts: [] })),
  http.get("*/get_image", () => new Response(null, { status: 204 })),
  http.post("*/team/new", () => jsonResponse({ team_id: `team-${Date.now()}` })),
  http.post("*/user/new", () => jsonResponse({ user_id: `user-${Date.now()}` })),
];
