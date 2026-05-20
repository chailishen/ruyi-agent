import { mockDefaultRole } from "@/mocks/config";

function base64UrlEncode(value: string): string {
  if (typeof btoa !== "undefined") {
    return btoa(value).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  return Buffer.from(value, "utf8")
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

export function createMockJwt(userRole: string = mockDefaultRole()): string {
  const payload = {
    key: "sk-mock-prototype-bearer",
    user_id: "mock-user-001",
    user_email: "admin@prototype.local",
    user_role: userRole,
    login_method: "username_password",
    premium_user: true,
    disabled_non_admin_personal_key_creation: false,
    exp: Math.floor(Date.now() / 1000) + 60 * 60 * 24 * 365,
  };
  const header = base64UrlEncode(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = base64UrlEncode(JSON.stringify(payload));
  return `${header}.${body}.prototype-mock-signature`;
}

export const MOCK_ACCESS_TOKEN = createMockJwt();
