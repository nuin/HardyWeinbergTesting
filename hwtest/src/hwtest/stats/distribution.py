"""Distribution functions for statistical tests.

Replaces the original [CHISQDIS] and [FACTORIAL] subroutines with
scipy-backed implementations.
"""

from __future__ import annotations

import numpy as np
from scipy.special import gammaln
from scipy.stats import chi2


def chi2_p_value(statistic: float, df: int) -> float:
    """Compute p-value from chi-squared distribution.

    Replaces the original [CHISQDIS] subroutine (lines 1291-1304).
    """
    if statistic <= 0:
        return 1.0
    return float(chi2.sf(statistic, df))


def log_factorial(n: int) -> float:
    """Compute log(n!) using scipy's gammaln.

    Replaces the original [FACTORIAL] subroutine (lines 1306-1311).
    gammaln(n+1) = log(n!) for non-negative integers.
    """
    if n < 0:
        return 0.0
    return float(gammaln(n + 1))


def log_factorial_array(max_n: int) -> np.ndarray:
    """Pre-compute log-factorials from 0 to max_n.

    Replaces the original F() array used in [SIMULATION] (line 1370).
    """
    return np.array([gammaln(i + 1) for i in range(max_n + 1)])
