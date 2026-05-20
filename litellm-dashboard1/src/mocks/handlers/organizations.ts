import { http } from "msw";
import { getOrganizationsList } from "@/mocks/mockStore";
import { jsonResponse } from "@/mocks/utils";

export const organizationsHandlers = [
  http.get("*/organization/list", () => jsonResponse(getOrganizationsList())),
  http.get("*/organization/info", ({ request }) => {
    const url = new URL(request.url);
    const id = url.searchParams.get("organization_id");
    const orgs = getOrganizationsList();
    return jsonResponse(orgs.find((o) => o.organization_id === id) ?? orgs[0] ?? {});
  }),
  http.post("*/organization/new", () => jsonResponse({ organization_id: `org-${Date.now()}` })),
  http.post("*/organization/update", () => jsonResponse({ status: "ok" })),
  http.post("*/organization/delete", () => jsonResponse({ status: "ok" })),
];
