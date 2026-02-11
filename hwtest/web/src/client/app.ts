import { AlleleSelector } from "./components/AlleleSelector.js";
import { TestSelector } from "./components/TestSelector.js";
import { DataEntry } from "./components/DataEntry.js";
import { ResultsTable } from "./components/ResultsTable.js";
import { TernaryPlot } from "./components/TernaryPlot.js";

interface TestResult {
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
  test_results: TestResult[];
}

class HWTestApp {
  private nAlleles = 2;
  private alleleSelector: AlleleSelector;
  private testSelector: TestSelector;
  private dataEntry: DataEntry;
  private resultsTable: ResultsTable;
  private ternaryPlot: TernaryPlot;

  constructor() {
    this.alleleSelector = new AlleleSelector();
    this.testSelector = new TestSelector();
    this.dataEntry = new DataEntry();
    this.resultsTable = new ResultsTable();
    this.ternaryPlot = new TernaryPlot();

    this.setupEventListeners();
  }

  private setupEventListeners(): void {
    document.getElementById("btn-next-alleles")?.addEventListener("click", () => {
      const input = document.getElementById("n-alleles") as HTMLInputElement;
      const n = parseInt(input.value);
      if (n < 2 || n > 12 || isNaN(n)) {
        alert("Choose a number between 2 and 12.");
        return;
      }
      this.nAlleles = n;
      this.showStep("step-input");
      this.testSelector.render(
        document.getElementById("test-selector")!,
        n
      );
      this.dataEntry.render(
        document.getElementById("data-entry")!,
        n
      );
    });

    document.getElementById("btn-back")?.addEventListener("click", () => {
      this.showStep("step-alleles");
    });

    document.getElementById("btn-run")?.addEventListener("click", () => {
      this.runTests();
    });

    document.getElementById("btn-new")?.addEventListener("click", () => {
      this.showStep("step-alleles");
    });
  }

  private showStep(stepId: string): void {
    document.querySelectorAll(".step").forEach((el) => el.classList.add("hidden"));
    document.getElementById(stepId)?.classList.remove("hidden");
  }

  private async runTests(): Promise<void> {
    const tests = this.testSelector.getSelectedTests();
    const data = this.dataEntry.getData(this.nAlleles);

    if (!data) return;

    const body: Record<string, unknown> = { ...data, tests };

    try {
      const response = await fetch("/api/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const err = await response.json();
        alert(`Error: ${err.detail || "Unknown error"}`);
        return;
      }

      const result: ApiResponse = await response.json();
      this.showStep("step-results");
      this.resultsTable.render(
        document.getElementById("results-table")!,
        result
      );
      this.ternaryPlot.render(
        document.getElementById("ternary-plot")!,
        result,
        this.nAlleles
      );
    } catch {
      alert("Failed to connect to the server. Is the backend running?");
    }
  }
}

new HWTestApp();
