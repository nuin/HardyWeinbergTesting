import { defineConfig, devices } from "@playwright/test";

// Browser tests for the Vite SPA in src/client. The FastAPI backend is not
// started: each test stubs POST /api/test with page.route(), so the suite
// checks the client (inputs, request body, results table, De Finetti plot)
// and needs nothing but Node and a Playwright browser.
const PORT = Number(process.env.PW_PORT ?? 5174);

export default defineConfig({
  testDir: "e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? "github" : "list",
  use: {
    baseURL: `http://localhost:${PORT}`,
    trace: "retain-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: `npx vite --port ${PORT} --strictPort`,
    url: `http://localhost:${PORT}`,
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});
