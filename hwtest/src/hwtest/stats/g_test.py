"""G-test (log-likelihood ratio test) for Hardy-Weinberg equilibrium.

Implements two variants: without correction and with Williams' continuity
correction, translated from the original Liberty BASIC code.
"""

from __future__ import annotations

import math

from hwtest.models import TestResult, TestType, TwoAlleleInput
from hwtest.stats.distribution import chi2_p_value

EPS = 1e-19


def g_test_no_correction(data: TwoAlleleInput) -> TestResult:
    """G-test (log-likelihood) without correction.

    Original lines 237-254:
    G = 2 * [D*log(D) + 2*(H/2)*log(H/2) + R*log(R)
            - 2*(D+H/2)*log(D+H/2) - 2*(H/2+R)*log(H/2+R)
            + N*log(N)]
    """
    d, h, r = data.d, data.h, data.r
    n = data.n

    d1 = d if d > 0 else EPS
    h1 = h / 2 if h > 0 else EPS
    r1 = r if r > 0 else EPS

    gt = d1 * math.log(d1) + 2 * h1 * math.log(h1) + r1 * math.log(r1)
    gt -= 2 * (d1 + h1) * math.log(d1 + h1)
    gt -= 2 * (h1 + r1) * math.log(h1 + r1)
    gt += n * math.log(n)
    g_stat = gt * 2

    p_value = chi2_p_value(g_stat, df=1)

    return TestResult(
        test_type=TestType.G_TEST,
        statistic=g_stat,
        p_value=p_value,
        df=1,
        label="G (log-likelihood) test without correction",
    )


def g_test_corrected(data: TwoAlleleInput) -> TestResult:
    """G-test with continuity correction.

    Original lines 256-276. The correction direction depends on
    whether DR < (H/2)^2 (excess heterozygosity) or not.
    """
    d, h, r = data.d, data.h, data.r
    n = data.n

    d1 = float(d) if d > 0 else EPS
    h1 = h / 2 if h > 0 else EPS
    r1 = float(r) if r > 0 else EPS

    # Apply continuity correction based on direction of deviation
    if d1 * r1 < h1 * h1:
        # Excess heterozygosity: increase homozygotes, decrease heterozygotes
        d1 = d1 + 0.5
        r1 = r1 + 0.5
        if h1 >= 1:
            h1 = h1 - 0.5
    else:
        # Excess homozygosity: decrease homozygotes, increase heterozygotes
        if d1 >= 1:
            d1 = d1 - 0.5
        if r1 >= 1:
            r1 = r1 - 0.5
        h1 = h1 + 0.5

    gt = d1 * math.log(d1) + 2 * h1 * math.log(h1) + r1 * math.log(r1)
    gt -= 2 * (d1 + h1) * math.log(d1 + h1)
    gt -= 2 * (h1 + r1) * math.log(h1 + r1)
    gt += n * math.log(n)
    g_stat = gt * 2

    p_value = chi2_p_value(g_stat, df=1)

    return TestResult(
        test_type=TestType.G_TEST_CORRECTED,
        statistic=g_stat,
        p_value=p_value,
        df=1,
        label="G (log-likelihood) test with continuity correction",
    )
