interface TestOption {
  id: string;
  label: string;
  twoAlleleOnly: boolean;
}

const ALL_TESTS: TestOption[] = [
  { id: "chi_square", label: "Chi-square without correction", twoAlleleOnly: false },
  { id: "chi_square_yates", label: "Chi-square with Yates' correction", twoAlleleOnly: true },
  { id: "chi_square_hogben_levene", label: "Chi-square with Hogben/Levene correction", twoAlleleOnly: true },
  { id: "chi_square_cannings_edwards", label: "Chi-square with Cannings & Edwards correction", twoAlleleOnly: true },
  { id: "g_test", label: "G-test without correction", twoAlleleOnly: true },
  { id: "g_test_corrected", label: "G-test with continuity correction", twoAlleleOnly: true },
  { id: "fisher_exact", label: "Fisher's exact test", twoAlleleOnly: true },
  { id: "haldane_exact", label: "Haldane's exact test", twoAlleleOnly: true },
  { id: "monte_carlo", label: "Exact probability by simulation", twoAlleleOnly: false },
];

export class TestSelector {
  render(container: HTMLElement, nAlleles: number): void {
    container.textContent = "";
    const tests = ALL_TESTS.filter((t) => nAlleles === 2 || !t.twoAlleleOnly);

    const heading = document.createElement("h3");
    heading.textContent = "Statistical Tests";
    container.appendChild(heading);

    for (const t of tests) {
      const label = document.createElement("label");
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.value = t.id;
      if (t.id === "chi_square") checkbox.checked = true;
      label.appendChild(checkbox);
      label.appendChild(document.createTextNode(" " + t.label));
      container.appendChild(label);
    }

    const btnDiv = document.createElement("div");
    btnDiv.style.marginTop = "0.5rem";
    const selectAllBtn = document.createElement("button");
    selectAllBtn.id = "btn-select-all";
    selectAllBtn.className = "btn-secondary";
    selectAllBtn.style.fontSize = "0.8rem";
    selectAllBtn.style.padding = "0.25rem 0.75rem";
    selectAllBtn.textContent = "Select all";
    selectAllBtn.addEventListener("click", () => {
      container.querySelectorAll<HTMLInputElement>('input[type="checkbox"]').forEach(
        (cb) => (cb.checked = true)
      );
    });
    btnDiv.appendChild(selectAllBtn);
    container.appendChild(btnDiv);
  }

  getSelectedTests(): string[] {
    const checkboxes = document.querySelectorAll<HTMLInputElement>(
      '#test-selector input[type="checkbox"]:checked'
    );
    return Array.from(checkboxes).map((cb) => cb.value);
  }
}
