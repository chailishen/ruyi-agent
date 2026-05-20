import { http } from "msw";
import { getTeamsList } from "@/mocks/mockStore";
import { jsonResponse } from "@/mocks/utils";

export const teamsHandlers = [
  http.get("*/v2/team/list", () => jsonResponse(getTeamsList())),
  http.get("*/team/list", () => jsonResponse(getTeamsList().teams)),
  http.get("*/team/info", () => jsonResponse(getTeamsList().teams[0] ?? {})),
  http.post("*/team/new", () => jsonResponse({ team_id: `team-${Date.now()}` })),
  http.post("*/team/update", () => jsonResponse({ status: "ok" })),
  http.post("*/team/delete", () => jsonResponse({ status: "ok" })),
];
