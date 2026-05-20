import { http } from "msw";
import { createMockJwt } from "@/mocks/auth/tokens";
import uiConfig from "@/mocks/fixtures/ui-config.json";
import proxyUiSettings from "@/mocks/fixtures/proxy-ui-settings.json";
import userInfo from "@/mocks/fixtures/user-info.json";
import modelsAvailable from "@/mocks/fixtures/models-available.json";
import inProductNudges from "@/mocks/fixtures/in-product-nudges.json";
import { jsonResponse } from "@/mocks/utils";

export const globalHandlers = [
  http.get("*/litellm/.well-known/litellm-ui-config", () => jsonResponse(uiConfig)),

  http.get("*/sso/get/ui_settings", () => jsonResponse(proxyUiSettings)),

  http.get("*/v2/user/info", () => jsonResponse(userInfo)),

  http.get("*/models", () => jsonResponse(modelsAvailable)),

  http.get("*/in_product_nudges", () => jsonResponse(inProductNudges)),

  http.get("*/health/readiness/details", () =>
    jsonResponse({
      status: "healthy",
      db: "connected",
      litellm_version: "1.0.0-prototype",
      success_callbacks: [],
      use_aiohttp_transport: true,
      log_level: "INFO",
      is_detailed_debug: false,
    }),
  ),

  http.post("*/v2/login", () =>
    jsonResponse({
      token: createMockJwt(),
      redirect_url: "/",
    }),
  ),

  http.post("*/v3/login", () =>
    jsonResponse({
      token: createMockJwt(),
      redirect_url: "/",
    }),
  ),

  http.post("*/v3/login/exchange", () =>
    jsonResponse({
      token: createMockJwt(),
      redirect_url: "/",
    }),
  ),
];
