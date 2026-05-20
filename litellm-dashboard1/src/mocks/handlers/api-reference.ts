import { http } from "msw";
import openapi from "@/mocks/fixtures/openapi-minimal.json";
import { jsonResponse } from "@/mocks/utils";

export const apiReferenceHandlers = [
  http.get("*/openapi.json", () => jsonResponse(openapi)),
];
