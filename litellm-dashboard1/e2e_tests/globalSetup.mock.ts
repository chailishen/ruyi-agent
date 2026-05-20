import { chromium } from "@playwright/test";
import { createMockJwt } from "../src/mocks/auth/tokens";
import { Role, STORAGE_PATHS } from "./fixtures/users";

const roleToJwtRole: Record<Role, string> = {
  [Role.ProxyAdmin]: "proxy_admin",
  [Role.ProxyAdminViewer]: "proxy_admin_viewer",
  [Role.InternalUser]: "internal_user",
  [Role.InternalUserViewer]: "internal_user_viewer",
  [Role.TeamAdmin]: "internal_user",
};

async function globalSetup() {
  const browser = await chromium.launch();

  for (const role of Object.values(Role)) {
    const storagePath = STORAGE_PATHS[role];
    const token = createMockJwt(roleToJwtRole[role]);

    const context = await browser.newContext();
    await context.addCookies([
      {
        name: "token",
        value: token,
        domain: "localhost",
        path: "/",
        sameSite: "Lax",
      },
    ]);
    await context.storageState({ path: storagePath });
    await context.close();
  }

  await browser.close();
}

export default globalSetup;
