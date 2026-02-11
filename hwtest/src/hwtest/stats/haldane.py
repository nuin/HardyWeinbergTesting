"""Haldane's exact test for Hardy-Weinberg equilibrium.

Translated from the original Liberty BASIC code (lines 344-366).
Enumerates all possible heterozygote counts with the same allele
counts and sums probabilities of configurations as extreme or more
extreme than the observed.
"""

from __future__ import annotations

import math

from hwtest.models import TestResult, TestType, TwoAlleleInput
from hwtest.stats.distribution import log_factorial


def haldane_exact_test(data: TwoAlleleInput) -> TestResult:
    """Haldane's exact test for HW equilibrium.

    Enumerates all possible H values (from HMIN to HMAX, step 2)
    that are compatible with the observed allele counts P and Q.
    Sums probabilities of all configurations that are as probable
    or less probable than the observed configuration.
    """
    d, h, r = data.d, data.h, data.r
    n = data.n
    p_count = data.p_count  # 2D + H
    q_count = data.q_count  # H + 2R

    # HMIN: 0 if H is even, 1 if H is odd
    hmin = 0 if h % 2 == 0 else 1

    # HMAX: min(P, Q) — but original uses: Q if D > R else P
    if d > r:
        hmax = q_count
    else:
        hmax = p_count

    # Pre-compute constant factorials
    nfac = log_factorial(n)
    n2fac = log_factorial(2 * n)
    pfac = log_factorial(p_count)
    qfac = log_factorial(q_count)
    constfac = nfac - n2fac + pfac + qfac

    # Probability of the observed configuration
    dfac = log_factorial(d)
    hfac = log_factorial(h)
    rfac = log_factorial(r)
    log_prob_obs = constfac - dfac - hfac - rfac + h * math.log(2)
    prob_obs = math.exp(log_prob_obs)

    # Sum probabilities of all configs as extreme or more
    probt = 0.0
    for h9 in range(hmin, hmax + 1, 2):
        d9 = (p_count - h9) // 2
        r9 = (q_count - h9) // 2

        d9fac = log_factorial(d9)
        h9fac = log_factorial(h9)
        r9fac = log_factorial(r9)

        log_prob = constfac - d9fac - h9fac - r9fac + h9 * math.log(2)
        prob = math.exp(log_prob)

        if prob <= prob_obs:
            probt += prob

    return TestResult(
        test_type=TestType.HALDANE_EXACT,
        statistic=None,
        p_value=probt,
        df=None,
        label="Haldane's exact test",
    )
