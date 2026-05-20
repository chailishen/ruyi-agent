import { http } from "msw";
import modelsAvailable from "@/mocks/fixtures/models-available.json";
import { jsonResponse } from "@/mocks/utils";

export const modelsHandlers = [
  http.get("*/model/info", () =>
    jsonResponse({
      data: [
        {
          model_name: "gpt-4o",
          litellm_params: { model: "openai/gpt-4o" },
          model_info: { id: "model-001" },
        },
      ],
    }),
  ),
  http.get("*/v1/model/info", () =>
    jsonResponse({
      data: [{ model_name: "gpt-4o", model_info: { id: "model-001" } }],
    }),
  ),
  http.get("*/credentials", () => jsonResponse([])),
  http.get("*/public/providers/fields", () => jsonResponse({ providers: [] })),
  http.post("*/model/new", () => jsonResponse({ model_id: `model-${Date.now()}` })),
  http.post("*/model/delete", () => jsonResponse({ status: "ok" })),
];
