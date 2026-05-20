import { http } from "msw";
import { createMockJwt } from "@/mocks/auth/tokens";
import { jsonResponse } from "@/mocks/utils";

export const onboardingHandlers = [
  http.get("*/onboarding/get_token", () =>
    jsonResponse({
      token: createMockJwt("internal_user"),
      user_id: "mock-invite-user",
      user_email: "invite@prototype.local",
    }),
  ),

  http.post("*/onboarding/claim_token", () =>
    jsonResponse({
      token: createMockJwt("internal_user"),
      redirect_url: "/",
    }),
  ),
];
