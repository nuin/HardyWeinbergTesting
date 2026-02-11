const ALLELE_NAMES = "ABCDEFGHIJKLMNO";

export class DataEntry {
  render(container: HTMLElement, nAlleles: number): void {
    container.textContent = "";

    const heading = document.createElement("h3");
    heading.textContent =
      nAlleles === 2 ? "Genotype Data" : `Genotype Data (${nAlleles} alleles)`;
    container.appendChild(heading);

    const grid = document.createElement("div");
    grid.className = "genotype-grid";

    if (nAlleles === 2) {
      this.addField(grid, "D = N(AA):", "input-d");
      this.addField(grid, "H = N(Aa):", "input-h");
      this.addField(grid, "R = N(aa):", "input-r");
    } else {
      for (let i = 0; i < nAlleles; i++) {
        for (let j = i; j < nAlleles; j++) {
          const label = ALLELE_NAMES[i] + ALLELE_NAMES[j] + ":";
          this.addField(grid, label, `g-${i}-${j}`);
        }
      }
    }

    container.appendChild(grid);
  }

  private addField(grid: HTMLElement, labelText: string, inputId: string): void {
    const label = document.createElement("label");
    label.textContent = labelText;
    grid.appendChild(label);

    const input = document.createElement("input");
    input.type = "number";
    input.id = inputId;
    input.min = "0";
    input.placeholder = "0";
    grid.appendChild(input);
  }

  getData(nAlleles: number): Record<string, unknown> | null {
    if (nAlleles === 2) {
      const d = this.getInt("input-d");
      const h = this.getInt("input-h");
      const r = this.getInt("input-r");
      if (d === null || h === null || r === null) {
        alert("Please enter valid non-negative integers.");
        return null;
      }
      return { d, h, r };
    }

    const genotypes: number[][] = Array.from({ length: nAlleles }, () =>
      Array(nAlleles).fill(0)
    );

    for (let i = 0; i < nAlleles; i++) {
      for (let j = i; j < nAlleles; j++) {
        const val = this.getInt(`g-${i}-${j}`);
        if (val === null) {
          alert("Please enter valid non-negative integers for all genotypes.");
          return null;
        }
        genotypes[i][j] = val;
      }
    }

    return { genotypes, n_alleles: nAlleles };
  }

  private getInt(id: string): number | null {
    const el = document.getElementById(id) as HTMLInputElement | null;
    if (!el || el.value === "") return null;
    const val = parseInt(el.value);
    if (isNaN(val) || val < 0) return null;
    return val;
  }
}
