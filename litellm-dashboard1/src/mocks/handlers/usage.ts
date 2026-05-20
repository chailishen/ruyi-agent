import { http } from "msw";
import globalActivity from "@/mocks/fixtures/global-activity.json";
import { jsonResponse } from "@/mocks/utils";

const perModelActivity = [
  {
    model: "gpt-4o",
    daily_data: globalActivity.daily_data,
  },
  {
    model: "claude-3-5-sonnet",
    daily_data: globalActivity.daily_data.map((d) => ({
      ...d,
      api_requests: Math.floor(d.api_requests * 0.6),
      total_tokens: Math.floor(d.total_tokens * 0.6),
      spend: d.spend * 0.6,
    })),
  },
];

export const usageHandlers = [
  http.get("*/global/activity", () => jsonResponse(globalActivity)),
  http.get("*/global/activity/model", () => jsonResponse(perModelActivity)),
  http.get("*/global/activity/cache_hits", () => jsonResponse({ daily_data: [] })),
  http.get("*/user/daily/activity", () => jsonResponse({ results: [], total_pages: 1 })),
  http.get("*/tag/daily/activity", () => jsonResponse({ spend_per_tag: [] })),
  http.get("*/team/daily/activity", () => jsonResponse({ results: [] })),
  http.get("*/spend/tags", () => jsonResponse({ spend_per_tag: [] })),
  http.get("*/user/filter", () => jsonResponse({ users: [] })),
  http.get("*/spend/logs", () => jsonResponse([])),
];
