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
  if (p === null) return "-";
  if (p >= 1e-4) return p.toFixed(4);
  if (p >= 1e-5) return "< 10\u207B\u2074";
  if (p >= 1e-6) return "< 10\u207B\u2075";
  return "< 10\u207B\u2076";
}

export class ResultsTable {
  render(container: HTMLElement, data: ApiResponse): void {
    container.textContent = "";

    // Header
    const header = document.createElement("h2");
    header.textContent = "Results";
    container.appendChild(header);

    // Allele frequencies
    const freqDiv = document.createElement("div");
    freqDiv.style.marginBottom = "1rem";
    freqDiv.style.fontFamily = "'Courier New', monospace";
    freqDiv.style.fontSize = "0.85rem";

    if (data.type === "two_allele" && data.p_freq !== undefined && data.q_freq !== undefined) {
      this.addLine(freqDiv, `p = P(A) = ${data.p_freq.toFixed(4)}`);
      this.addLine(freqDiv, `q = P(a) = ${data.q_freq.toFixed(4)}`);
    } else if (data.allele_freqs) {
      data.allele_freqs.forEach((f, i) => {
        this.addLine(freqDiv, `P(${String.fromCharCode(65 + i)}) = ${f.toFixed(4)}`);
      });
    }
    container.appendChild(freqDiv);

    // Separator
    container.appendChild(this.createSeparator());

    // Test results table
    const table = document.createElement("table");
    table.style.width = "100%";
    table.style.borderCollapse = "collapse";
    table.style.fontSize = "0.82rem";

    // Header row
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    for (const text of ["Test", "Statistic", "df", "P-value"]) {
      const th = document.createElement("th");
      th.textContent = text;
      th.style.textAlign = text === "Test" ? "left" : "right";
      th.style.padding = "0.4rem 0.5rem";
      th.style.borderBottom = "2px solid #ddd";
      th.style.fontSize = "0.8rem";
      th.style.color = "#555";
      headerRow.appendChild(th);
    }
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Body
    const tbody = document.createElement("tbody");
    for (const tr of data.test_results) {
      const row = document.createElement("tr");

      const isSignificant = tr.p_value !== null && tr.p_value < 0.05;
      if (isSignificant) {
        row.style.color = "#dc2626";
        row.style.fontWeight = "600";
      }

      // Test name
      const tdName = document.createElement("td");
      tdName.textContent = tr.label;
      tdName.style.padding = "0.35rem 0.5rem";
      tdName.style.borderBottom = "1px solid #eee";
      row.appendChild(tdName);

      // Statistic
      const tdStat = document.createElement("td");
      tdStat.textContent = tr.statistic !== null ? tr.statistic.toFixed(4) : "-";
      tdStat.style.textAlign = "right";
      tdStat.style.padding = "0.35rem 0.5rem";
      tdStat.style.borderBottom = "1px solid #eee";
      tdStat.style.fontFamily = "'Courier New', monospace";
      row.appendChild(tdStat);

      // df
      const tdDf = document.createElement("td");
      tdDf.textContent = tr.df !== null ? String(tr.df) : "-";
      tdDf.style.textAlign = "right";
      tdDf.style.padding = "0.35rem 0.5rem";
      tdDf.style.borderBottom = "1px solid #eee";
      tdDf.style.fontFamily = "'Courier New', monospace";
      row.appendChild(tdDf);

      // P-value
      const tdP = document.createElement("td");
      tdP.textContent = formatPValue(tr.p_value);
      tdP.style.textAlign = "right";
      tdP.style.padding = "0.35rem 0.5rem";
      tdP.style.borderBottom = "1px solid #eee";
      tdP.style.fontFamily = "'Courier New', monospace";
      row.appendChild(tdP);

      tbody.appendChild(row);
    }
    table.appendChild(tbody);
    container.appendChild(table);
  }

  private addLine(parent: HTMLElement, text: string): void {
    const div = document.createElement("div");
    div.textContent = text;
    parent.appendChild(div);
  }

  private createSeparator(): HTMLElement {
    const hr = document.createElement("hr");
    hr.style.border = "none";
    hr.style.borderTop = "1px solid #ddd";
    hr.style.margin = "0.75rem 0";
    return hr;
  }
}
