# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HW_TEST is a tool for testing the null hypothesis of Hardy-Weinberg equilibrium proportions using genotype data from autosomal genetic markers with 2 to 12 alleles.

Published: Santos, Lemes & Otto (2020) - DOI: https://doi.org/10.1590/1678-4685-GMB-2019-0380

## Source Code

### Original (Legacy)
The original program is `HW_TEST_v.1.1.bas` (~1430 lines of Liberty BASIC v4.04, Windows-only). The compiled distribution lives in `HW_TEST_v.1.1/`.

### Python Rewrite (`hwtest/`)
Modern Python package with full test coverage:

```
hwtest/
  pyproject.toml                  # hatchling build, deps: numpy, scipy, pydantic
  src/hwtest/
    models.py                     # Data models (TwoAlleleInput, MultiAlleleInput, TestResult, etc.)
    validators.py                 # Input validation
    engine.py                     # Orchestrator: run selected tests, collect results
    results.py                    # Text + JSON output formatting
    stats/
      common.py                   # Allele frequency calculation
      distribution.py             # chi2 p-value (scipy), log-factorial (gammaln)
      chi_square.py               # 4 two-allele variants + multi-allele
      g_test.py                   # With and without continuity correction
      fisher.py                   # Fisher's exact test
      haldane.py                  # Haldane's exact test
      monte_carlo.py              # Two-allele and multi-allele simulation
    plotting/ternary.py           # De Finetti diagram (matplotlib)
    io/file_parser.py             # Parse .txt input files
    cli.py                        # Typer CLI entry point
    tui.py                        # Textual TUI
    api.py                        # FastAPI backend
  tests/                          # pytest test suite (64 tests)
```

### TypeScript Web Frontend (`hwtest/web/`)
SPA that calls the Python FastAPI backend:
```
web/
  src/server/index.ts             # Express proxy server
  src/client/                     # Vite + TypeScript SPA with D3.js ternary plot
```

## Development Commands

```bash
cd hwtest
uv venv .venv && source .venv/bin/activate
uv pip install -e ".[all]"       # Install all dependencies
python3 -m pytest tests/ -v      # Run tests
hwtest run -a 2 -d 119,42,39     # CLI usage
```

## Statistical Tests

Test selection uses `set[TestType]` enum (replaces original bitmask):

| TestType enum value | Test |
|---------------------|------|
| `chi_square` | Chi-square without correction |
| `chi_square_yates` | Chi-square with Yates' correction |
| `chi_square_hogben_levene` | Chi-square with Hogben/Levene correction |
| `chi_square_cannings_edwards` | Chi-square with Cannings & Edwards correction |
| `g_test` | G (log-likelihood) test without correction |
| `g_test_corrected` | Log-likelihood test with continuity correction |
| `fisher_exact` | Fisher's exact test |
| `haldane_exact` | Haldane's exact test |
| `monte_carlo` | Exact probability by Monte Carlo simulation |

Multi-allele (k > 2) only supports: `chi_square` and `monte_carlo`.

## Key Constraints

- Maximum population size (N): 1000 individuals
- Allele count range: 2-12
- Minimum sample size: 3
- Both alleles must be present (P > 0, Q > 0)

## Validation Fixtures

1. **Two-allele**: D=119, H=42, R=39 → p=0.7, q=0.3, all p-values < 10⁻⁶
2. **Four-allele**: AA=2,AB=4,AC=6,AD=8,BB=10,BC=12,BD=14,CC=16,CD=18,DD=20 → chi-sq p≈0.0465
