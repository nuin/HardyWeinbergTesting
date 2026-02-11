"""Textual TUI for Hardy-Weinberg equilibrium testing.

Three-screen flow matching the original windows:
1. Allele count entry (Win000)
2. Test selection checkboxes + data entry (Win001/Win004)
3. Scrollable results display (Win002/Win005)
"""

from __future__ import annotations

try:
    from textual.app import App, ComposeResult
    from textual.containers import Center, Horizontal, Vertical, VerticalScroll
    from textual.screen import Screen
    from textual.widgets import (
        Button,
        Checkbox,
        Footer,
        Header,
        Input,
        Label,
        Static,
    )
except ImportError as e:
    raise ImportError(
        "TUI dependencies not installed. Install with: pip install hwtest[tui]"
    ) from e

from hwtest.engine import run_multi_allele, run_two_allele
from hwtest.models import TestType
from hwtest.results import format_multi_allele_text, format_two_allele_text
from hwtest.validators import ValidationError, validate_multi_allele, validate_two_allele


class AlleleScreen(Screen):
    """Screen 1: Enter number of alleles."""

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="allele-form"):
                yield Label("HARDY-WEINBERG EQUILIBRIUM TEST", id="title")
                yield Label("Copyright 2006-2019 by Santos, Lemes & Otto")
                yield Label("Universidade de Sao Paulo")
                yield Label("")
                yield Label("Number of alleles (2-12):")
                yield Input(placeholder="2", id="n-alleles", type="integer")
                yield Button("Next", id="next-btn", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next-btn":
            n_input = self.query_one("#n-alleles", Input)
            try:
                n = int(n_input.value)
                if n < 2 or n > 12:
                    self.notify("Choose a number between 2 and 12.", severity="error")
                    return
                self.app.n_alleles = n  # type: ignore[attr-defined]
                if n == 2:
                    self.app.push_screen(TwoAlleleScreen())
                else:
                    self.app.push_screen(MultiAlleleScreen())
            except ValueError:
                self.notify("Please enter a valid number.", severity="error")


class TwoAlleleScreen(Screen):
    """Screen 2a: Two-allele test selection and data entry."""

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="test-panel"):
                yield Label("Statistical Tests", id="tests-title")
                yield Checkbox("Chi-square without correction", id="cb-chi", value=True)
                yield Checkbox("Chi-square with Yates' correction", id="cb-yates")
                yield Checkbox("Chi-square with Hogben/Levene", id="cb-hogben")
                yield Checkbox("Chi-square with Cannings & Edwards", id="cb-ce")
                yield Checkbox("G-test without correction", id="cb-g")
                yield Checkbox("G-test with continuity correction", id="cb-g-corr")
                yield Checkbox("Fisher's exact test", id="cb-fisher")
                yield Checkbox("Haldane's exact test", id="cb-haldane")
                yield Checkbox("Exact probability by simulation", id="cb-mc")
                yield Button("Select all", id="select-all-btn")
            with Vertical(id="data-panel"):
                yield Label("Genotype Data", id="data-title")
                yield Label("D = N(AA):")
                yield Input(placeholder="0", id="input-d", type="integer")
                yield Label("H = N(Aa):")
                yield Input(placeholder="0", id="input-h", type="integer")
                yield Label("R = N(aa):")
                yield Input(placeholder="0", id="input-r", type="integer")
                yield Button("Run", id="run-btn", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "select-all-btn":
            for cb in self.query(Checkbox):
                cb.value = True
        elif event.button.id == "run-btn":
            self._run_tests()

    def _run_tests(self) -> None:
        try:
            d = int(self.query_one("#input-d", Input).value)
            h = int(self.query_one("#input-h", Input).value)
            r = int(self.query_one("#input-r", Input).value)
        except ValueError:
            self.notify("Please enter valid integers.", severity="error")
            return

        try:
            data = validate_two_allele(d, h, r)
        except ValidationError as e:
            self.notify(str(e), severity="error")
            return

        test_map = {
            "cb-chi": TestType.CHI_SQUARE,
            "cb-yates": TestType.CHI_SQUARE_YATES,
            "cb-hogben": TestType.CHI_SQUARE_HOGBEN_LEVENE,
            "cb-ce": TestType.CHI_SQUARE_CANNINGS_EDWARDS,
            "cb-g": TestType.G_TEST,
            "cb-g-corr": TestType.G_TEST_CORRECTED,
            "cb-fisher": TestType.FISHER_EXACT,
            "cb-haldane": TestType.HALDANE_EXACT,
            "cb-mc": TestType.MONTE_CARLO,
        }
        selected = {v for k, v in test_map.items() if self.query_one(f"#{k}", Checkbox).value}
        if not selected:
            selected = {TestType.CHI_SQUARE}

        results = run_two_allele(data, tests=selected)
        text = format_two_allele_text(results)
        self.app.push_screen(ResultsScreen(text))


class MultiAlleleScreen(Screen):
    """Screen 2b: Multi-allele test selection and data entry."""

    def compose(self) -> ComposeResult:
        yield Header()
        n = self.app.n_alleles  # type: ignore[attr-defined]
        allele_names = "ABCDEFGHIJKLMNO"

        with Vertical():
            yield Label("Statistical Tests")
            yield Checkbox("Chi-square without correction", id="cb-chi-multi", value=True)
            yield Checkbox("Exact probability by simulation", id="cb-mc-multi")
            yield Label("")
            yield Label(f"Genotype Data ({n} alleles)")

            for i in range(n):
                for j in range(i, n):
                    label = f"{allele_names[i]}{allele_names[j]}"
                    with Horizontal():
                        yield Label(f"  {label}: ")
                        yield Input(placeholder="0", id=f"g-{i}-{j}", type="integer")

            yield Button("Run", id="run-multi-btn", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run-multi-btn":
            self._run_tests()

    def _run_tests(self) -> None:
        n = self.app.n_alleles  # type: ignore[attr-defined]
        genotypes = [[0] * n for _ in range(n)]

        try:
            for i in range(n):
                for j in range(i, n):
                    val = int(self.query_one(f"#g-{i}-{j}", Input).value)
                    genotypes[i][j] = val
        except ValueError:
            self.notify("Please enter valid integers.", severity="error")
            return

        try:
            data = validate_multi_allele(genotypes, n)
        except ValidationError as e:
            self.notify(str(e), severity="error")
            return

        selected: set[TestType] = set()
        if self.query_one("#cb-chi-multi", Checkbox).value:
            selected.add(TestType.CHI_SQUARE)
        if self.query_one("#cb-mc-multi", Checkbox).value:
            selected.add(TestType.MONTE_CARLO)
        if not selected:
            selected = {TestType.CHI_SQUARE}

        results = run_multi_allele(data, tests=selected)
        text = format_multi_allele_text(results)
        self.app.push_screen(ResultsScreen(text))


class ResultsScreen(Screen):
    """Screen 3: Scrollable results display."""

    def __init__(self, results_text: str) -> None:
        super().__init__()
        self._results_text = results_text

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll():
            yield Static(self._results_text, id="results-output")
        with Center():
            yield Button("Back", id="back-btn")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()


class HWTestApp(App):
    """Hardy-Weinberg Equilibrium Test TUI Application."""

    TITLE = "HW_TEST"
    CSS = """
    #title { text-style: bold; }
    #allele-form { width: 60; padding: 2; }
    #test-panel { width: 50%; padding: 1; }
    #data-panel { width: 50%; padding: 1; }
    """

    n_alleles: int = 2

    def on_mount(self) -> None:
        self.push_screen(AlleleScreen())


def main() -> None:
    app = HWTestApp()
    app.run()


if __name__ == "__main__":
    main()
