"""Property-based tests for the statistics in ``hwtest.stats``.

The example-based tests pin the manual's fixtures. These generate genotype
counts across the whole valid input space (validators.py: N in [3, 1000],
both alleles present) and check invariants that must hold for every sample:

* every p-value is a probability;
* relabelling the alleles (swapping AA and aa) changes nothing;
* the two-allele chi-square equals the general k-allele formula at k = 2;
* Haldane's exact test agrees with an independent enumeration of the
  exact conditional distribution of heterozygote counts;
* the multi-allele chi-square is invariant to the order of the alleles.
"""

from __future__ import annotations

import math

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from hwtest.models import MultiAlleleInput, TwoAlleleInput
from hwtest.stats.chi_square import (
    chi_square_cannings_edwards,
    chi_square_hogben_levene,
    chi_square_multi_allele,
    chi_square_no_correction,
    chi_square_yates,
)
from hwtest.stats.fisher import fisher_exact_test
from hwtest.stats.g_test import g_test_corrected, g_test_no_correction
from hwtest.stats.haldane import haldane_exact_test
from hwtest.validators import validate_multi_allele, validate_two_allele

# Floating-point slack for sums of many small probabilities.
TOL = 1e-9

DETERMINISTIC_TWO_ALLELE_TESTS = [
    chi_square_no_correction,
    chi_square_yates,
    chi_square_hogben_levene,
    chi_square_cannings_edwards,
    g_test_no_correction,
    g_test_corrected,
    fisher_exact_test,
    haldane_exact_test,
]


@st.composite
def two_allele_samples(draw: st.DrawFn, max_n: int = 1000) -> TwoAlleleInput:
    """Genotype counts (D, H, R) that pass ``validate_two_allele``."""
    d = draw(st.integers(min_value=0, max_value=max_n))
    h = draw(st.integers(min_value=0, max_value=max_n - d))
    r = draw(st.integers(min_value=0, max_value=max_n - d - h))
    n = d + h + r
    assume(n >= 3)
    assume(2 * d + h > 0 and h + 2 * r > 0)
    return validate_two_allele(d, h, r)


@st.composite
def multi_allele_samples(draw: st.DrawFn) -> MultiAlleleInput:
    """Upper-triangular genotype matrices that pass ``validate_multi_allele``."""
    k = draw(st.integers(min_value=3, max_value=6))
    cells = [(i, j) for i in range(k) for j in range(i, k)]
    counts = draw(
        st.lists(st.integers(min_value=0, max_value=40), min_size=len(cells), max_size=len(cells))
    )
    genotypes = [[0] * k for _ in range(k)]
    for (i, j), c in zip(cells, counts):
        genotypes[i][j] = c
    data = MultiAlleleInput(genotypes=genotypes, n_alleles=k)
    assume(3 <= data.n <= 1000)
    assume(all(c > 0 for c in data.allele_counts))
    return validate_multi_allele(genotypes, k)


def _swap_alleles(data: TwoAlleleInput) -> TwoAlleleInput:
    return validate_two_allele(data.r, data.h, data.d)


def _haldane_reference(data: TwoAlleleInput) -> float:
    """Exact HWE p-value by direct enumeration (Emigh 1980; Wigginton et al. 2005).

    P(H = h | N, nA) = N! nA! nB! 2^h / ((nA+nB)! D! h! R!), summed over all
    h with the same parity as nA whose probability does not exceed the
    observed one. Written independently of ``haldane.py``: it works from
    min(nA, nB) and uses math.lgamma rather than scipy.
    """
    n, n_a, n_b = data.n, data.p_count, data.q_count

    def log_prob(h: int) -> float:
        d = (n_a - h) // 2
        r = (n_b - h) // 2
        return (
            math.lgamma(n + 1)
            + math.lgamma(n_a + 1)
            + math.lgamma(n_b + 1)
            - math.lgamma(2 * n + 1)
            - math.lgamma(d + 1)
            - math.lgamma(h + 1)
            - math.lgamma(r + 1)
            + h * math.log(2)
        )

    observed = log_prob(data.h)
    total = 0.0
    for h in range(n_a % 2, min(n_a, n_b) + 1, 2):
        lp = log_prob(h)
        # Same comparison as haldane.py, which compares exp() values.
        if math.exp(lp) <= math.exp(observed):
            total += math.exp(lp)
    return total


@pytest.mark.parametrize("test_fn", DETERMINISTIC_TWO_ALLELE_TESTS, ids=lambda f: f.__name__)
@given(data=two_allele_samples())
def test_p_value_is_a_probability(test_fn, data: TwoAlleleInput) -> None:
    result = test_fn(data)
    if result.p_value is None:
        # Only Fisher may decline, and only for the documented degenerate samples.
        assert test_fn is fisher_exact_test
        assert data.h == 1 and (data.d == 0 or data.r == 0)
        return
    assert not math.isnan(result.p_value)
    assert -TOL <= result.p_value <= 1 + TOL


@pytest.mark.parametrize("test_fn", DETERMINISTIC_TWO_ALLELE_TESTS, ids=lambda f: f.__name__)
@given(data=two_allele_samples())
def test_relabelling_alleles_changes_nothing(test_fn, data: TwoAlleleInput) -> None:
    """Calling A 'a' and a 'A' is the same sample: statistic and p-value must match."""
    original = test_fn(data)
    swapped = test_fn(_swap_alleles(data))

    if original.p_value is None or swapped.p_value is None:
        assert original.p_value is None and swapped.p_value is None
    else:
        assert swapped.p_value == pytest.approx(original.p_value, rel=1e-9, abs=1e-12)

    if original.statistic is not None:
        assert swapped.statistic == pytest.approx(original.statistic, rel=1e-9, abs=1e-9)


@given(data=two_allele_samples())
def test_two_allele_chi_square_matches_general_formula(data: TwoAlleleInput) -> None:
    """At k = 2 the sum over genotype cells of (O-E)^2/E is the closed form N*(H^2-4DR)^2/(PQ)^2."""
    as_matrix = MultiAlleleInput(genotypes=[[data.d, data.h], [0, data.r]], n_alleles=2)
    closed_form = chi_square_no_correction(data)
    general = chi_square_multi_allele(as_matrix)
    assert general.df == 1
    assert general.statistic == pytest.approx(closed_form.statistic, rel=1e-9, abs=1e-9)
    assert general.p_value == pytest.approx(closed_form.p_value, rel=1e-9, abs=1e-12)


@given(data=two_allele_samples(max_n=400))
def test_haldane_matches_independent_enumeration(data: TwoAlleleInput) -> None:
    result = haldane_exact_test(data)
    assert result.p_value == pytest.approx(_haldane_reference(data), rel=1e-9, abs=1e-12)


@given(data=two_allele_samples())
def test_haldane_p_value_is_at_least_the_observed_probability(data: TwoAlleleInput) -> None:
    """The observed configuration is always in its own tail, so p > 0."""
    result = haldane_exact_test(data)
    assert result.p_value is not None
    assert result.p_value > 0


@given(data=multi_allele_samples(), perm_seed=st.randoms(use_true_random=False))
@settings(deadline=None)
def test_multi_allele_chi_square_ignores_allele_order(data: MultiAlleleInput, perm_seed) -> None:
    k = data.n_alleles
    order = list(range(k))
    perm_seed.shuffle(order)

    permuted = [[0] * k for _ in range(k)]
    for i in range(k):
        for j in range(i, k):
            a, b = sorted((order[i], order[j]))
            permuted[a][b] += data.genotypes[i][j]

    original = chi_square_multi_allele(data)
    relabelled = chi_square_multi_allele(validate_multi_allele(permuted, k))
    assert relabelled.df == original.df
    assert relabelled.statistic == pytest.approx(original.statistic, rel=1e-9, abs=1e-9)
    assert relabelled.p_value == pytest.approx(original.p_value, rel=1e-9, abs=1e-12)
    assert -TOL <= original.p_value <= 1 + TOL
