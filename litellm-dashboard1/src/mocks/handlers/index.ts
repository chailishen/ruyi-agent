import { globalHandlers } from "@/mocks/handlers/global";
import { keysHandlers } from "@/mocks/handlers/keys";
import { teamsHandlers } from "@/mocks/handlers/teams";
import { usersHandlers } from "@/mocks/handlers/users";
import { modelsHandlers } from "@/mocks/handlers/models";
import { usageHandlers } from "@/mocks/handlers/usage";
import { logsHandlers } from "@/mocks/handlers/logs";
import { hubPublicHandlers } from "@/mocks/handlers/hub-public";
import { settingsHandlers } from "@/mocks/handlers/settings";
import { organizationsHandlers } from "@/mocks/handlers/organizations";
import { mcpHandlers } from "@/mocks/handlers/mcp";
import { guardrailsHandlers } from "@/mocks/handlers/guardrails";
import { playgroundHandlers } from "@/mocks/handlers/playground";
import { apiReferenceHandlers } from "@/mocks/handlers/api-reference";
import { onboardingHandlers } from "@/mocks/handlers/onboarding";
import { commonHandlers } from "@/mocks/handlers/common";

export const handlers = [
  ...globalHandlers,
  ...keysHandlers,
  ...teamsHandlers,
  ...usersHandlers,
  ...organizationsHandlers,
  ...modelsHandlers,
  ...usageHandlers,
  ...logsHandlers,
  ...hubPublicHandlers,
  ...settingsHandlers,
  ...mcpHandlers,
  ...guardrailsHandlers,
  ...playgroundHandlers,
  ...apiReferenceHandlers,
  ...onboardingHandlers,
  ...commonHandlers,
];
