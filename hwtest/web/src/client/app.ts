import { TestSelector } from "./components/TestSelector.js";
import { DataEntry } from "./components/DataEntry.js";
import { ResultsTable } from "./components/ResultsTable.js";
import { TernaryPlot } from "./components/TernaryPlot.js";

interface TestResultItem {
  test: string;
  label: string;
  statistic: number | null;
  p_value: number | null;
  df: number | null;
}

interface ApiResponse {
  type: string;
  p_freq?: number;
  q_freq?: number;
  allele_freqs?: number[];
  test_results: TestResultItem[];
}

class HWTestApp {
  private testSelector: TestSelector;
  private dataEntry: DataEntry;
  private resultsTable: ResultsTable;
  private ternaryPlot: TernaryPlot;

  constructor() {
    this.testSelector = new TestSelector();
    this.dataEntry = new DataEntry();
    this.resultsTable = new ResultsTable();
    this.ternaryPlot = new TernaryPlot();

    this.init();
  }

  private init(): void {
    const nAllelesInput = document.getElementById("n-alleles") as HTMLInputElement;
    const testContainer = document.getElementById("test-selector")!;
    const dataContainer = document.getElementById("data-entry")!;

    // Initial render
    const n = parseInt(nAllelesInput.value);
    this.testSelector.render(testContainer, n);
    this.dataEntry.render(dataContainer, n);

    // Re-render when allele count changes
    nAllelesInput.addEventListener("change", () => {
      const newN = parseInt(nAllelesInput.value);
      if (newN >= 2 && newN <= 12) {
        this.testSelector.render(testContainer, newN);
        this.dataEntry.render(dataContainer, newN);
        document.getElementById("results-section")?.classList.add("hidden");
      }
    });

    document.getElementById("btn-run")?.addEventListener("click", () => {
      this.runTests();
    });
  }

  private async runTests(): Promise<void> {
    const nAllelesInput = document.getElementById("n-alleles") as HTMLInputElement;
    const nAlleles = parseInt(nAllelesInput.value);
    const tests = this.testSelector.getSelectedTests();
    const data = this.dataEntry.getData(nAlleles);
    const statusMsg = document.getElementById("status-msg")!;
    const btn = document.getElementById("btn-run") as HTMLButtonElement;

    if (!data) return;

    const body: Record<string, unknown> = { ...data, tests };

    btn.disabled = true;
    statusMsg.textContent = "Running tests...";

    try {
      const response = await fetch("/api/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const err = await response.json();
        statusMsg.textContent = `Error: ${err.detail || "Unknown error"}`;
        btn.disabled = false;
        return;
      }

      const result: ApiResponse = await response.json();
      statusMsg.textContent = "";

      document.getElementById("results-section")?.classList.remove("hidden");
      this.resultsTable.render(document.getElementById("results-table")!, result);
      this.ternaryPlot.render(document.getElementById("ternary-plot")!, result, nAlleles);

      document.getElementById("results-section")?.scrollIntoView({ behavior: "smooth" });
    } catch {
      statusMsg.textContent = "Failed to connect. Is the backend running?";
    } finally {
      btn.disabled = false;
    }
  }
}

new HWTestApp();
