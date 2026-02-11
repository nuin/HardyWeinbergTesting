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

function formatPValue(p: number | null): string {
  if (p === null) return "   -";
  if (p >= 1e-4) return ` = ${p.toFixed(4)}`;
  if (p >= 1e-5) return " < 10^-4";
  if (p >= 1e-6) return " < 10^-5";
  return " < 10^-6";
}

export class ResultsTable {
  render(container: HTMLElement, data: ApiResponse): void {
    let text = "";
    text += "HARDY-WEINBERG EQUILIBRIUM TESTING\n";
    text += "==================================\n\n";

    if (data.type === "two_allele") {
      text += `p = P(A) = ${data.p_freq?.toFixed(4) ?? "-"}\n`;
      text += `q = P(a) = ${data.q_freq?.toFixed(4) ?? "-"}\n\n`;
    } else if (data.allele_freqs) {
      text += "Allele frequencies:\n";
      data.allele_freqs.forEach((f, i) => {
        text += `  ${String.fromCharCode(65 + i)}: ${f.toFixed(4)}\n`;
      });
      text += "\n";
    }

    text += "Test Results:\n";
    text += "-".repeat(60) + "\n";

    for (const tr of data.test_results) {
      const stat =
        tr.statistic !== null ? `  statistic = ${tr.statistic.toFixed(4)}` : "";
      const df = tr.df !== null ? `  df = ${tr.df}` : "";
      text += `P(${tr.label})${formatPValue(tr.p_value)}\n`;
      if (stat || df) {
        text += `    ${stat}${df}\n`;
      }
    }

    container.textContent = text;
  }
}
