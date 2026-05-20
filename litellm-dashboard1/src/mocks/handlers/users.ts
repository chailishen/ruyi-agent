import { http } from "msw";
import { getUsersList } from "@/mocks/mockStore";
import userInfo from "@/mocks/fixtures/user-info.json";
import { jsonResponse } from "@/mocks/utils";

export const usersHandlers = [
  http.get("*/user/list", () => jsonResponse(getUsersList())),
  http.get("*/user/info", () => jsonResponse(userInfo)),
  http.post("*/user/new", () => jsonResponse({ user_id: `user-${Date.now()}` })),
  http.post("*/user/delete", () => jsonResponse({ status: "ok" })),
];
