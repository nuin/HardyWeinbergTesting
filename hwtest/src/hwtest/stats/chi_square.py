"""Chi-square tests for Hardy-Weinberg equilibrium.

Implements four two-allele variants and the multi-allele generalized
chi-square test, translated from the original Liberty BASIC code.
"""

from __future__ import annotations

from hwtest.models import (
    MultiAlleleInput,
    TestResult,
    TestType,
    TwoAlleleInput,
)
from hwtest.stats.distribution import chi2_p_value

EPS = 1e-19


def chi_square_no_correction(data: TwoAlleleInput) -> TestResult:
    """Chi-square test without correction.

    Original lines 188-196:
    CH(1) = N * (H*H - 4*D*R)^2 / (P*Q)^2
    """
    d, h, r = data.d, data.h, data.r
    n = data.n
    p_count = data.p_count  # 2D + H
    q_count = data.q_count  # H + 2R

    chi2_stat = n * (h * h - 4 * d * r) ** 2 / (p_count * q_count) ** 2
    p_value = chi2_p_value(chi2_stat, df=1)

    return TestResult(
        test_type=TestType.CHI_SQUARE,
        statistic=chi2_stat,
        p_value=p_value,
        df=1,
        label="Chi-square without correction",
    )


def expected_no_correction(data: TwoAlleleInput) -> tuple[float, float, float]:
    """Expected frequencies under standard HW (no correction).

    DE0 = P^2 / (4N), HE0 = P*Q / (2N), RE0 = Q^2 / (4N)
    """
    n = data.n
    p = data.p_count
    q = data.q_count
    de0 = p**2 / (4 * n)
    he0 = p * q / (2 * n)
    re0 = q**2 / (4 * n)
    return de0, he0, re0


def chi_square_yates(data: TwoAlleleInput) -> TestResult:
    """Chi-square test with Yates' continuity correction.

    Original lines 198-205:
    CH(2) = N * (|H*H - 4*D*R| - 2*N)^2 / (P*Q)^2
    """
    d, h, r = data.d, data.h, data.r
    n = data.n
    p_count = data.p_count
    q_count = data.q_count

    chi2_stat = n * (abs(h * h - 4 * d * r) - 2 * n) ** 2 / (p_count * q_count) ** 2
    p_value = chi2_p_value(chi2_stat, df=1)

    return TestResult(
        test_type=TestType.CHI_SQUARE_YATES,
        statistic=chi2_stat,
        p_value=p_value,
        df=1,
        label="Chi-square with Yates' correction",
    )


def chi_square_hogben_levene(data: TwoAlleleInput) -> TestResult:
    """Chi-square test with Hogben/Levene correction.

    Original lines 207-220. Uses unbiased expected frequencies:
    DE1 = P(P-1) / [2(2N-1)]
    HE1 = P*Q / (2N-1)
    RE1 = Q(Q-1) / [2(2N-1)]
    chi2 = D^2/DE1 + H^2/HE1 + R^2/RE1 - N
    """
    d, h, r = data.d, data.h, data.r
    n = data.n
    p = data.p_count
    q = data.q_count

    de1 = p * (p - 1) / (2 * (2 * n - 1))
    he1 = p * q / (2 * n - 1)
    re1 = q * (q - 1) / (2 * (2 * n - 1))

    # Avoid division by zero
    if de1 == 0:
        de1 = EPS
    if he1 == 0:
        he1 = EPS
    if re1 == 0:
        re1 = EPS

    chi2_stat = d**2 / de1 + h**2 / he1 + r**2 / re1 - n
    p_value = chi2_p_value(chi2_stat, df=1)

    return TestResult(
        test_type=TestType.CHI_SQUARE_HOGBEN_LEVENE,
        statistic=chi2_stat,
        p_value=p_value,
        df=1,
        label="Chi-square with Hogben/Levene correction",
    )


def expected_hogben_levene(data: TwoAlleleInput) -> tuple[float, float, float]:
    """Expected frequencies under Hogben/Levene correction."""
    n = data.n
    p = data.p_count
    q = data.q_count
    de1 = p * (p - 1) / (2 * (2 * n - 1))
    he1 = p * q / (2 * n - 1)
    re1 = q * (q - 1) / (2 * (2 * n - 1))
    return de1, he1, re1


def chi_square_cannings_edwards(data: TwoAlleleInput) -> TestResult:
    """Chi-square test with Cannings & Edwards correction.

    Original lines 222-235:
    DE2 = (P^2 - H) / (4N)
    HE2 = (P*Q + H) / (2N)
    RE2 = (Q^2 - H) / (4N)
    chi2 = D^2/DE2 + H^2/HE2 + R^2/RE2 - N
    """
    d, h, r = data.d, data.h, data.r
    n = data.n
    p = data.p_count
    q = data.q_count

    de2 = (p**2 - h) / (4 * n)
    he2 = (p * q + h) / (2 * n)
    re2 = (q**2 - h) / (4 * n)

    if de2 == 0:
        de2 = EPS
    if he2 == 0:
        he2 = EPS
    if re2 == 0:
        re2 = EPS

    chi2_stat = d**2 / de2 + h**2 / he2 + r**2 / re2 - n
    p_value = chi2_p_value(chi2_stat, df=1)

    return TestResult(
        test_type=TestType.CHI_SQUARE_CANNINGS_EDWARDS,
        statistic=chi2_stat,
        p_value=p_value,
        df=1,
        label="Chi-square with Cannings & Edwards correction",
    )


def expected_cannings_edwards(data: TwoAlleleInput) -> tuple[float, float, float]:
    """Expected frequencies under Cannings & Edwards correction."""
    n = data.n
    p = data.p_count
    q = data.q_count
    h = data.h
    de2 = (p**2 - h) / (4 * n)
    he2 = (p * q + h) / (2 * n)
    re2 = (q**2 - h) / (4 * n)
    return de2, he2, re2


def chi_square_multi_allele(data: MultiAlleleInput) -> TestResult:
    """Generalized chi-square test for k > 2 alleles.

    Original lines 1091-1107:
    Sum over all genotype cells of (O - E)^2 / E
    where E = p_i * p_j * N (homozygote) or 2 * p_i * p_j * N (heterozygote).
    df = k(k-1)/2
    """
    k = data.n_alleles
    n = data.n
    freqs = data.allele_freqs

    chi2_stat = 0.0
    for i in range(k):
        for j in range(i, k):
            observed = data.genotypes[i][j]
            if i == j:
                expected = freqs[i] * freqs[j] * n
            else:
                expected = 2 * freqs[i] * freqs[j] * n
            if expected > 0:
                chi2_stat += (observed - expected) ** 2 / expected

    df = k * (k - 1) // 2
    p_value = chi2_p_value(chi2_stat, df=df)

    return TestResult(
        test_type=TestType.CHI_SQUARE,
        statistic=chi2_stat,
        p_value=p_value,
        df=df,
        label="Chi-square without correction (multi-allele)",
    )
