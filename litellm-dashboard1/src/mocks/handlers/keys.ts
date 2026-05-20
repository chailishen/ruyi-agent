import { http } from "msw";
import { addKey, deleteKey, getKeysList } from "@/mocks/mockStore";
import { jsonResponse } from "@/mocks/utils";

export const keysHandlers = [
  http.get("*/key/list", () => jsonResponse(getKeysList())),

  http.get("*/key/info", ({ request }) => {
    const url = new URL(request.url);
    const key = url.searchParams.get("key") ?? url.searchParams.get("keys");
    const list = getKeysList();
    const found = list.keys.find((k) => k.token === key || k.token_id === key);
    return jsonResponse(found ?? list.keys[0] ?? {});
  }),

  http.post("*/key/generate", async () => {
    const id = `key-${Date.now()}`;
    addKey({
      ...getKeysList().keys[0],
      token: `sk-mock-${id}`,
      token_id: id,
      key_alias: `new-key-${id}`,
      key_name: `sk-...${id.slice(-6)}`,
      spend: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
    return jsonResponse({
      key: `sk-mock-${id}`,
      key_name: `sk-...${id.slice(-6)}`,
    });
  }),

  http.post("*/key/delete", async ({ request }) => {
    try {
      const body = (await request.json()) as { keys?: string[] };
      const toDelete = body?.keys ?? [];
      toDelete.forEach((k) => deleteKey(k));
    } catch {
      /* query param fallback */
    }
    return jsonResponse({ deleted_keys: [] });
  }),

  http.get("*/key/aliases", () =>
    jsonResponse({
      aliases: ["engineering-default", "data-pipeline"],
      total_count: 2,
      current_page: 1,
      total_pages: 1,
      size: 50,
    }),
  ),
];
