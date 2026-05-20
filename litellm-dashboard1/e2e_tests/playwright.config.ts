import { defineConfig, devices } from "@playwright/test";

const useMockMode = process.env.PLAYWRIGHT_MOCK_MODE === "true";
const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? (useMockMode ? "http://localhost:3000" : "http://localhost:4000");

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: ".",
  testMatch: ["**/*.spec.ts", "**/*.setup.ts"],
  testIgnore: ["**/*.test.*"],
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: "html",
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL,

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: "on-first-retry",

    /* Action timeout for clicks, fills, waitForSelector, etc. */
    actionTimeout: 15 * 1000,
    navigationTimeout: 30 * 1000,
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],

  /* Timeout settings */
  timeout: 3 * 60 * 1000,
  expect: {
    timeout: 10 * 1000,
  },
  globalSetup: require.resolve(useMockMode ? "./globalSetup.mock" : "./globalSetup"),
});
