"""Command-line interface for Hardy-Weinberg equilibrium testing."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

try:
    import typer
    from rich.console import Console
except ImportError as e:
    raise ImportError(
        "CLI dependencies not installed. Install with: pip install hwtest[cli]"
    ) from e

from hwtest.engine import run_multi_allele, run_two_allele
from hwtest.io.file_parser import parse_data_string, parse_multi_allele_file, parse_two_allele_file
from hwtest.models import MultiAlleleInput, TestType, TwoAlleleInput
from hwtest.results import (
    format_multi_allele_text,
    format_two_allele_text,
    results_to_json,
)

app = typer.Typer(
    name="hwtest",
    help="Hardy-Weinberg Equilibrium Testing (Santos, Lemes & Otto, 2020)",
    no_args_is_help=True,
)
console = Console()


class OutputFormat(str, Enum):
    text = "text"
    json = "json"


@app.command()
def run(
    alleles: Annotated[int, typer.Option("--alleles", "-a", help="Number of alleles (2-12)")] = 2,
    data: Annotated[Optional[str], typer.Option("--data", "-d", help="Comma-separated genotype counts")] = None,
    file: Annotated[Optional[Path], typer.Option("--file", "-f", help="Input file path")] = None,
    tests: Annotated[str, typer.Option("--tests", "-t", help="Tests to run: 'all' or comma-separated list")] = "all",
    format: Annotated[OutputFormat, typer.Option("--format", help="Output format")] = OutputFormat.text,
    seed: Annotated[Optional[int], typer.Option("--seed", "-s", help="Random seed for Monte Carlo")] = None,
    simulations: Annotated[int, typer.Option("--simulations", help="Number of Monte Carlo simulations")] = 1000,
    plot: Annotated[Optional[Path], typer.Option("--plot", "-p", help="Save ternary plot to file")] = None,
) -> None:
    """Run Hardy-Weinberg equilibrium tests on genotype data."""
    if data is None and file is None:
        console.print("[red]Error:[/red] Either --data or --file must be provided.")
        raise typer.Exit(1)

    # Parse test selection
    selected_tests: set[TestType] | None = None
    if tests != "all":
        test_names = [t.strip() for t in tests.split(",")]
        selected_tests = set()
        for name in test_names:
            try:
                selected_tests.add(TestType(name))
            except ValueError:
                console.print(f"[red]Error:[/red] Unknown test '{name}'. Valid tests: {[t.value for t in TestType]}")
                raise typer.Exit(1)

    # Parse input data
    if alleles == 2:
        if data is not None:
            input_data = parse_data_string(data, 2)
        else:
            input_data = parse_two_allele_file(file)  # type: ignore[arg-type]
        assert isinstance(input_data, TwoAlleleInput)
        results = run_two_allele(input_data, tests=selected_tests, mc_seed=seed, mc_simulations=simulations)
        if format == OutputFormat.text:
            console.print(format_two_allele_text(results))
        else:
            console.print(results_to_json(results))
    else:
        if data is not None:
            input_data = parse_data_string(data, alleles)
        else:
            input_data = parse_multi_allele_file(file, alleles)  # type: ignore[arg-type]
        assert isinstance(input_data, MultiAlleleInput)
        results = run_multi_allele(input_data, tests=selected_tests, mc_seed=seed, mc_simulations=simulations)
        if format == OutputFormat.text:
            console.print(format_multi_allele_text(results))
        else:
            console.print(results_to_json(results))

    # Ternary plot (two-allele only with Monte Carlo)
    if plot is not None and alleles == 2 and hasattr(results, "bootstrap") and results.bootstrap is not None:
        try:
            from hwtest.plotting.ternary import save_ternary_plot
            save_ternary_plot(results, str(plot))
            console.print(f"Ternary plot saved to {plot}")
        except ImportError:
            console.print("[yellow]Warning:[/yellow] matplotlib not installed. Install with: pip install hwtest[plot]")


if __name__ == "__main__":
    app()
