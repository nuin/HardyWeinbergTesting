import { expect, test, type Page, type Request } from "@playwright/test";

// Shape returned by hwtest/src/hwtest/api.py for the manual's two-allele
// fixture (D=119, H=42, R=39). Values are illustrative; the client only
// formats what it is given.
const TWO_ALLELE_RESPONSE = {
  type: "two_allele",
  n: 200,
  d: 119,
  h: 42,
  r: 39,
  p_freq: 0.7,
  q_freq: 0.3,
  test_results: [
    { test: "chi_square", label: "Chi-square without correction", statistic: 46.9, p_value: 7.3e-12, df: 1 },
    { test: "haldane_exact", label: "Haldane's exact test", statistic: null, p_value: 0.2345, df: null },
  ],
};

async function stubApi(page: Page, body: unknown, status = 200): Promise<Request[]> {
  const seen: Request[] = [];
  await page.route("**/api/test", async (route) => {
    seen.push(route.request());
    await route.fulfill({ status, contentType: "application/json", body: JSON.stringify(body) });
  });
  return seen;
}

// Blur the field so the browser fires exactly one native "change", which is
// what app.ts listens for; then wait for the re-rendered genotype grid.
async function setAlleleCount(page: Page, k: number): Promise<void> {
  await page.locator("#n-alleles").fill(String(k));
  await page.locator("#n-alleles").press("Tab");
  await expect(page.locator("#data-entry h3")).toHaveText(`Genotype Data (${k} alleles)`);
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test("renders the two-allele form by default", async ({ page }) => {
  await expect(page).toHaveTitle("Hardy-Weinberg Equilibrium Test");
  await expect(page.locator("#input-d")).toBeVisible();
  await expect(page.locator("#input-h")).toBeVisible();
  await expect(page.locator("#input-r")).toBeVisible();

  const checkboxes = page.locator('#test-selector input[type="checkbox"]');
  await expect(checkboxes).toHaveCount(9);
  await expect(page.locator('#test-selector input[value="chi_square"]')).toBeChecked();
  await expect(page.locator("#results-section")).toBeHidden();
});

test("switching to four alleles shows the genotype matrix and multi-allele tests only", async ({
  page,
}) => {
  await setAlleleCount(page, 4);

  // k(k+1)/2 = 10 genotype cells for k = 4
  await expect(page.locator('#data-entry input[id^="g-"]')).toHaveCount(10);
  await expect(page.locator("#input-d")).toHaveCount(0);

  const tests = page.locator('#test-selector input[type="checkbox"]');
  await expect(tests).toHaveCount(2);
  await expect(tests.nth(0)).toHaveValue("chi_square");
  await expect(tests.nth(1)).toHaveValue("monte_carlo");
});

test("runs a two-allele test and renders the table and De Finetti plot", async ({ page }) => {
  const requests = await stubApi(page, TWO_ALLELE_RESPONSE);

  await page.locator("#input-d").fill("119");
  await page.locator("#input-h").fill("42");
  await page.locator("#input-r").fill("39");
  await page.locator("#btn-select-all").click();
  await page.locator("#btn-run").click();

  await expect(page.locator("#results-section")).toBeVisible();
  expect(requests).toHaveLength(1);
  const sent = requests[0].postDataJSON();
  expect(sent).toMatchObject({ d: 119, h: 42, r: 39 });
  expect(sent.tests).toHaveLength(9);

  const results = page.locator("#results-table");
  await expect(results).toContainText("p = P(A) = 0.7000");
  await expect(results).toContainText("q = P(a) = 0.3000");

  const rows = results.locator("tbody tr");
  await expect(rows).toHaveCount(2);
  await expect(rows.nth(0)).toContainText("46.9000");
  await expect(rows.nth(0)).toContainText("< 10⁻⁶");
  await expect(rows.nth(1)).toContainText("0.2345");

  const plot = page.locator("#ternary-plot svg");
  await expect(plot).toHaveCount(1);
  expect(await plot.locator("circle").count()).toBeGreaterThan(0);
  await expect(page.locator("#btn-run")).toBeEnabled();
});

test("multi-allele runs send the genotype matrix and skip the plot", async ({ page }) => {
  const requests = await stubApi(page, {
    type: "multi_allele",
    allele_freqs: [0.1, 0.2, 0.7],
    test_results: [
      { test: "chi_square", label: "Chi-square without correction (multi-allele)", statistic: 3.2, p_value: 0.36, df: 3 },
    ],
  });

  await setAlleleCount(page, 3);
  const cells = page.locator('#data-entry input[id^="g-"]');
  for (let i = 0; i < 6; i++) await cells.nth(i).fill(String(i + 1));
  await page.locator("#btn-run").click();

  await expect(page.locator("#results-table")).toContainText("P(C) = 0.7000");
  const sent = requests[0].postDataJSON();
  expect(sent.n_alleles).toBe(3);
  expect(sent.genotypes).toEqual([
    [1, 2, 3],
    [0, 4, 5],
    [0, 0, 6],
  ]);
  await expect(page.locator("#ternary-plot svg")).toHaveCount(0);
});

test("shows the backend's validation message", async ({ page }) => {
  await stubApi(page, { detail: "Sample size N=2 is too small. Minimum is 3." }, 422);

  await page.locator("#input-d").fill("1");
  await page.locator("#input-h").fill("1");
  await page.locator("#input-r").fill("0");
  await page.locator("#btn-run").click();

  await expect(page.locator("#status-msg")).toHaveText(
    "Error: Sample size N=2 is too small. Minimum is 3.",
  );
  await expect(page.locator("#results-section")).toBeHidden();
  await expect(page.locator("#btn-run")).toBeEnabled();
});

test("reports an unreachable backend", async ({ page }) => {
  await page.route("**/api/test", (route) => route.abort("connectionrefused"));

  await page.locator("#input-d").fill("10");
  await page.locator("#input-h").fill("20");
  await page.locator("#input-r").fill("10");
  await page.locator("#btn-run").click();

  await expect(page.locator("#status-msg")).toHaveText(
    "Failed to connect. Is the backend running?",
  );
});

test("blank genotype fields are rejected before any request", async ({ page }) => {
  const requests = await stubApi(page, TWO_ALLELE_RESPONSE);
  const messages: string[] = [];
  page.once("dialog", async (dialog) => {
    messages.push(dialog.message());
    await dialog.dismiss();
  });
  await page.locator("#btn-run").click();
  await expect.poll(() => messages).toEqual(["Please enter valid non-negative integers."]);
  expect(requests).toHaveLength(0);
  await expect(page.locator("#results-section")).toBeHidden();
});
