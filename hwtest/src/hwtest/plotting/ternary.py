"""De Finetti (ternary) diagram for Hardy-Weinberg equilibrium.

Translated from the original Liberty BASIC code (lines 744-850).
Coordinates:
  x = (D + H/2) / N  (allele frequency p)
  y = H / N          (heterozygote frequency)
HW parabola: y = 2p(1-p)
95% confidence bands: y = 2p(1-p)(1 +/- sqrt(3.8415/N))
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hwtest.models import TwoAlleleResults

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    raise ImportError(
        "Plotting dependencies not installed. Install with: pip install hwtest[plot]"
    ) from e


def create_ternary_plot(results: TwoAlleleResults) -> plt.Figure:
    """Create a De Finetti diagram from two-allele HW test results."""
    data = results.input_data
    d, h, r = data.d, data.h, data.r
    n = data.n
    p0 = results.p_freq

    crit_chi2 = 3.8415  # chi-squared critical value, alpha=0.05, df=1

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))

    # Triangle outline
    ax.plot([0, 0.5], [0, 1], "k-", linewidth=0.5)
    ax.plot([0.5, 1], [1, 0], "k-", linewidth=0.5)
    ax.plot([0, 1], [0, 0], "k-", linewidth=0.5)

    # HW equilibrium parabola
    p_vals = np.linspace(0, 1, 500)
    hw_h = 2 * p_vals * (1 - p_vals)
    ax.plot(p_vals, hw_h, "k-", linewidth=1.5, label="HW equilibrium")

    # 95% confidence bands
    if n > crit_chi2:
        f_val = math.sqrt(crit_chi2 / n)
        lower = 2 * p_vals * (1 - p_vals) * (1 - f_val)
        upper = 2 * p_vals * (1 - p_vals) * (1 + f_val)

        # Clip upper band to valid region
        for i in range(len(p_vals)):
            p = p_vals[i]
            f_neg = -f_val
            if f_neg * (1 - p) < -p or f_neg * p < p - 1:
                upper[i] = np.nan

        ax.plot(p_vals, lower, "k--", linewidth=0.5, alpha=0.5)
        ax.plot(p_vals, upper, "k--", linewidth=0.5, alpha=0.5)

    # Simulation points (if bootstrap available)
    if results.bootstrap is not None:
        bs = results.bootstrap
        # Expected (red dots)
        if bs.sim_points_expected:
            exp_x = [pt[0] for pt in bs.sim_points_expected]
            exp_y = [pt[1] for pt in bs.sim_points_expected]
            ax.scatter(exp_x, exp_y, c="red", s=4, alpha=0.3, label="Expected (simulated)")

        # Observed (black dots)
        if bs.sim_points_observed:
            obs_x = [pt[0] for pt in bs.sim_points_observed]
            obs_y = [pt[1] for pt in bs.sim_points_observed]
            ax.scatter(obs_x, obs_y, c="black", s=4, alpha=0.3, label="Observed (simulated)")

    # Sample point (blue)
    sample_x = (d + h / 2) / n
    sample_y = h / n
    exp_y_sample = 2 * p0 * (1 - p0)
    ax.scatter([sample_x], [sample_y], c="blue", s=50, zorder=5, label="Sample")
    ax.scatter([sample_x], [exp_y_sample], c="blue", s=50, zorder=5, marker="^", label="Expected")

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("p (allele frequency)", fontsize=12)
    ax.set_ylabel("h (heterozygote frequency)", fontsize=12)
    ax.set_title("De Finetti Diagram", fontsize=14)
    ax.legend(loc="upper right", fontsize=8)
    ax.set_aspect("equal")

    return fig


def save_ternary_plot(results: TwoAlleleResults, path: str) -> None:
    """Save the De Finetti diagram to a file."""
    fig = create_ternary_plot(results)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
