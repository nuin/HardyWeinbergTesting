"""Orchestrator: run selected tests and collect results."""

from __future__ import annotations

import math

from hwtest.models import (
    ALL_TWO_ALLELE_TESTS,
    MULTI_ALLELE_TESTS,
    BootstrapEstimates,
    ExpectedFrequencies,
    MultiAlleleInput,
    MultiAlleleResults,
    TestResult,
    TestType,
    TwoAlleleInput,
    TwoAlleleResults,
)
from hwtest.stats.chi_square import (
    chi_square_cannings_edwards,
    chi_square_hogben_levene,
    chi_square_multi_allele,
    chi_square_no_correction,
    chi_square_yates,
    expected_cannings_edwards,
    expected_hogben_levene,
    expected_no_correction,
)
from hwtest.stats.fisher import fisher_exact_test
from hwtest.stats.g_test import g_test_corrected, g_test_no_correction
from hwtest.stats.haldane import haldane_exact_test
from hwtest.stats.monte_carlo import monte_carlo_multi_allele, monte_carlo_two_allele


def run_two_allele(
    data: TwoAlleleInput,
    tests: set[TestType] | None = None,
    mc_seed: int | None = None,
    mc_simulations: int = 1000,
) -> TwoAlleleResults:
    """Run selected tests for a two-allele system.

    If tests is None, all tests are run.
    """
    if tests is None:
        tests = ALL_TWO_ALLELE_TESTS

    # Always compute expected frequencies
    ef_no = expected_no_correction(data)
    ef_hl = expected_hogben_levene(data)
    ef_ce = expected_cannings_edwards(data)

    expected = ExpectedFrequencies(
        no_correction=ef_no,
        hogben_levene=ef_hl,
        cannings_edwards=ef_ce,
    )

    p_freq = data.p_freq
    q_freq = data.q_freq
    n = data.n

    # Standard errors
    se_h0 = math.sqrt((p_freq + data.d / n - 2 * p_freq**2) / (2 * n))
    se_h1 = math.sqrt(p_freq * q_freq / (2 * n))

    results: list[TestResult] = []
    bootstrap: BootstrapEstimates | None = None

    # Dispatch to individual test functions
    dispatch: dict[TestType, object] = {
        TestType.CHI_SQUARE: chi_square_no_correction,
        TestType.CHI_SQUARE_YATES: chi_square_yates,
        TestType.CHI_SQUARE_HOGBEN_LEVENE: chi_square_hogben_levene,
        TestType.CHI_SQUARE_CANNINGS_EDWARDS: chi_square_cannings_edwards,
        TestType.G_TEST: g_test_no_correction,
        TestType.G_TEST_CORRECTED: g_test_corrected,
        TestType.FISHER_EXACT: fisher_exact_test,
        TestType.HALDANE_EXACT: haldane_exact_test,
    }

    for test_type in TestType:
        if test_type not in tests:
            continue
        if test_type == TestType.MONTE_CARLO:
            result, bootstrap = monte_carlo_two_allele(
                data, n_simulations=mc_simulations, seed=mc_seed
            )
            results.append(result)
        elif test_type in dispatch:
            fn = dispatch[test_type]
            results.append(fn(data))  # type: ignore[operator]

    return TwoAlleleResults(
        input_data=data,
        expected_frequencies=expected,
        p_freq=p_freq,
        q_freq=q_freq,
        se_h0=se_h0,
        se_h1=se_h1,
        test_results=results,
        bootstrap=bootstrap,
    )


def run_multi_allele(
    data: MultiAlleleInput,
    tests: set[TestType] | None = None,
    mc_seed: int | None = None,
    mc_simulations: int = 1000,
) -> MultiAlleleResults:
    """Run selected tests for a multi-allele (k > 2) system.

    Only chi-square and Monte Carlo simulation are available for k > 2.
    """
    if tests is None:
        tests = MULTI_ALLELE_TESTS

    # Filter to only supported multi-allele tests
    tests = tests & MULTI_ALLELE_TESTS

    results: list[TestResult] = []
    bootstrap: BootstrapEstimates | None = None

    if TestType.CHI_SQUARE in tests:
        results.append(chi_square_multi_allele(data))

    if TestType.MONTE_CARLO in tests:
        results.append(
            monte_carlo_multi_allele(data, n_simulations=mc_simulations, seed=mc_seed)
        )

    return MultiAlleleResults(
        input_data=data,
        allele_freqs=data.allele_freqs,
        test_results=results,
        bootstrap=bootstrap,
    )
