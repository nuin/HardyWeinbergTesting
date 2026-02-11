"""Fisher's exact test for Hardy-Weinberg equilibrium.

Translated from the original Liberty BASIC code (lines 288-342).
The test converts the genotype counts into a 2x2 contingency table
and computes the exact probability using the hypergeometric distribution.
"""

from __future__ import annotations

from hwtest.models import TestResult, TestType, TwoAlleleInput


def fisher_exact_test(data: TwoAlleleInput) -> TestResult:
    """Fisher's exact test for HW equilibrium.

    The original code transforms genotype counts (D, H, R) into a 2x2
    contingency table, then enumerates all tables with the same marginals
    to compute the exact two-sided p-value.

    Special case: if (D=0 and H=1) or (R=0 and H=1), the test is
    undefined (returns p_value=None).
    """
    d, h, r, n = data.d, data.h, data.r, data.n

    # Special case: test undefined
    if (d == 0 and h == 1) or (r == 0 and h == 1):
        return TestResult(
            test_type=TestType.FISHER_EXACT,
            statistic=None,
            p_value=None,
            df=None,
            label="Fisher's exact test (undefined for this sample)",
        )

    # Build 2x2 table from genotype counts
    # Following original code exactly (lines 298-324)
    a = d
    dd = r  # renamed to avoid shadowing

    if h % 2 == 0:
        b = h // 2
        c = h // 2
    else:
        if h > 1:
            b = (h + 1) // 2
            c = (h - 1) // 2
        else:
            b = 1
            c = 0

    e = a + c
    f = b + dd
    g = a + b
    hh = c + dd
    nn = g + hh

    # Ensure g <= h, e <= f, g <= e (normalize table)
    if g > hh:
        g, hh = hh, g
        a, c = c, a
        b, dd = dd, b
    if e > f:
        e, f = f, e
        a, b = b, a
        c, dd = dd, c
    if g > e:
        g, e = e, g
        f, hh = hh, f
        b, c = c, b
    if a > b:
        a, b = b, a
        c, dd = dd, c
        e, f = f, e

    # Compute probability using the FACTRL subroutine logic
    ad = a - e * g / nn

    # Compute P1 (probability of observed table)
    p1 = _factrl(a, g, e, f, nn)
    eps_fisher = p1 / 10000

    if p1 < 1e-8:
        pfish = 0.0
        return TestResult(
            test_type=TestType.FISHER_EXACT,
            statistic=None,
            p_value=pfish,
            df=None,
            label="Fisher's exact test",
        )

    if ad == 0:
        pr2 = (1 - p1) / 2
        pr3 = pr2
        pfish = p1 + pr2 + pr3
        return TestResult(
            test_type=TestType.FISHER_EXACT,
            statistic=None,
            p_value=pfish,
            df=None,
            label="Fisher's exact test",
        )

    # Sum probabilities of more extreme tables (left tail)
    pr2 = 0.0
    for i99 in range(a - 1, -1, -1):
        p2 = _factrl(i99, g, e, f, nn)
        if p1 > p2:
            pr2 += p2
        if p2 < eps_fisher:
            break

    # Sum probabilities of more extreme tables (right tail)
    pr3 = 0.0
    for i99 in range(a + 1, g + 1):
        p3 = _factrl(i99, g, e, f, nn)
        if p1 > p3:
            pr3 += p3
        if p3 < eps_fisher:
            break

    pfish = p1 + pr2 + pr3

    return TestResult(
        test_type=TestType.FISHER_EXACT,
        statistic=None,
        p_value=pfish,
        df=None,
        label="Fisher's exact test",
    )


def _factrl(i99: int, g: int, e: int, f: int, n: int) -> float:
    """Compute hypergeometric probability for a specific table.

    Translated from [FACTRL] subroutine (lines 1313-1321).
    Computes: P(X = i99) where X ~ Hypergeometric(N=n, K=g, n=e)
    but using the original's incremental product formulation.
    """
    p99 = 1.0
    for i6 in range(1, i99 + 1):
        p99 *= (g + i6 - i99) / (f + i6)
    for i6 in range(i99 + 1, e + 1):
        p99 *= (1 - g / (f + i6)) / (1 - i99 / i6)
    return p99
