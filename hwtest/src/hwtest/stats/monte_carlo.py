"""Monte Carlo simulation for Hardy-Weinberg exact probability estimation.

Translated from the original Liberty BASIC code:
- Two-allele: lines 596-731 (1000 simulations with bootstrap CIs)
- Multi-allele: lines 1369-1429 (1000 simulations via [SIMULATION])
"""

from __future__ import annotations

import math

import numpy as np

from hwtest.models import (
    BootstrapEstimates,
    GenotypeBootstrap,
    MultiAlleleInput,
    TestResult,
    TestType,
    TwoAlleleInput,
)
from hwtest.stats.distribution import log_factorial


def monte_carlo_two_allele(
    data: TwoAlleleInput,
    n_simulations: int = 1000,
    seed: int | None = None,
) -> tuple[TestResult, BootstrapEstimates]:
    """Monte Carlo exact probability estimation for two alleles.

    Simulates n_simulations datasets under HW equilibrium using the
    observed allele frequency, computes exact probability of each
    simulated dataset, and counts how many are <= the observed.
    Also collects bootstrap estimates for genotype frequencies.
    """
    rng = np.random.default_rng(seed)
    d, h, r = data.d, data.h, data.r
    n = data.n
    t = n_simulations

    p_count = data.p_count
    q_count = data.q_count
    p0 = p_count / (2 * n)

    # Expected frequencies under HW
    exp_d = p0**2
    exp_h = 2 * p0 * (1 - p0)

    # Constant factorial terms
    nfac = log_factorial(n)
    n2fac = log_factorial(2 * n)
    constfac = nfac - n2fac

    # Observed probability
    def _compute_prob(d1: int, h1: int, r1: int) -> float:
        p1 = 2 * d1 + h1
        q1 = h1 + 2 * r1
        pfac = log_factorial(p1)
        qfac = log_factorial(q1)
        dfac = log_factorial(d1)
        hfac = log_factorial(h1)
        rfac = log_factorial(r1)
        log_prob = constfac + pfac + qfac - dfac - hfac - rfac + h1 * math.log(2)
        return math.exp(log_prob)

    prob_obs = _compute_prob(d, h, r)

    # Storage for simulation results
    obs_d_arr = np.zeros(t)
    obs_h_arr = np.zeros(t)
    exp_d_arr = np.zeros(t)
    exp_h_arr = np.zeros(t)

    probt = 0
    p_total = 0.0

    for i in range(t):
        # Simulate under HW expected frequencies
        samples = rng.random(n)
        d1 = int(np.sum(samples <= exp_d))
        h1 = int(np.sum((samples > exp_d) & (samples < exp_d + exp_h)))
        r1 = n - d1 - h1

        # Simulate under observed frequencies
        obs_samples = rng.random(n)
        od1 = int(np.sum(obs_samples <= d / n))
        oh1 = int(np.sum((obs_samples > d / n) & (obs_samples <= (d + h) / n)))

        # Track allele frequency
        p1_count = 2 * d1 + h1
        p_total += p1_count / (2 * n)

        # Compare exact probabilities
        prob_sim = _compute_prob(d1, h1, r1)
        if prob_sim <= prob_obs:
            probt += 1

        obs_d_arr[i] = od1
        obs_h_arr[i] = oh1
        exp_d_arr[i] = d1
        exp_h_arr[i] = h1

    exact_p_value = probt / t
    mean_p = p_total / t

    # Build bootstrap estimates for each genotype
    bootstrap = _build_bootstrap(
        data, t, n, p0, exp_d, exp_h,
        obs_d_arr, obs_h_arr, exp_d_arr, exp_h_arr,
        exact_p_value, mean_p,
    )

    result = TestResult(
        test_type=TestType.MONTE_CARLO,
        statistic=None,
        p_value=exact_p_value,
        df=None,
        label="Exact probability by Monte Carlo simulation",
    )
    return result, bootstrap


def _build_bootstrap(
    data: TwoAlleleInput,
    t: int,
    n: int,
    p0: float,
    exp_d: float,
    exp_h: float,
    obs_d_arr: np.ndarray,
    obs_h_arr: np.ndarray,
    exp_d_arr: np.ndarray,
    exp_h_arr: np.ndarray,
    exact_p_value: float,
    mean_p: float,
) -> BootstrapEstimates:
    """Build bootstrap estimates matching the original output format."""
    d, h, r = data.d, data.h, data.r
    exp_r = (1 - p0) ** 2

    obs_r_arr = n - obs_d_arr - obs_h_arr
    exp_r_arr = n - exp_d_arr - exp_h_arr

    genotype_labels = ["AA", "Aa", "aa"]
    obs_arrays = [obs_d_arr / n, obs_h_arr / n, obs_r_arr / n]
    exp_arrays = [exp_d_arr / n, exp_h_arr / n, exp_r_arr / n]
    obs_freqs = [d / n, h / n, r / n]
    exp_freqs_hw = [exp_d, exp_h, exp_r]

    observed_bootstraps = []
    expected_bootstraps = []

    for idx, label in enumerate(genotype_labels):
        # Observed bootstrap
        obs_sorted = np.sort(obs_arrays[idx])
        obs_boot = GenotypeBootstrap(
            genotype_label=label,
            observed_freq=obs_freqs[idx],
            normal_ci=_normal_ci(obs_freqs[idx], n),
            bootstrap_mean=float(np.mean(obs_sorted)),
            bootstrap_median=float((obs_sorted[t // 2 - 1] + obs_sorted[t // 2]) / 2),
            bootstrap_ci=(float(obs_sorted[25]), float(obs_sorted[974])),
        )
        observed_bootstraps.append(obs_boot)

        # Expected bootstrap
        exp_sorted = np.sort(exp_arrays[idx])
        exp_boot = GenotypeBootstrap(
            genotype_label=label,
            observed_freq=exp_freqs_hw[idx],
            normal_ci=_expected_ci(idx, p0, n),
            bootstrap_mean=float(np.mean(exp_sorted)),
            bootstrap_median=float((exp_sorted[t // 2 - 1] + exp_sorted[t // 2]) / 2),
            bootstrap_ci=(float(exp_sorted[25]), float(exp_sorted[974])),
        )
        expected_bootstraps.append(exp_boot)

    # Ternary plot points
    sim_obs = [(float((obs_d_arr[i] + obs_h_arr[i] / 2) / n),
                float(obs_h_arr[i] / n)) for i in range(t)]
    sim_exp = [(float((exp_d_arr[i] + exp_h_arr[i] / 2) / n),
                float(exp_h_arr[i] / n)) for i in range(t)]

    return BootstrapEstimates(
        mean_p=mean_p,
        observed=observed_bootstraps,
        expected=expected_bootstraps,
        exact_p_value=exact_p_value,
        sim_points_observed=sim_obs,
        sim_points_expected=sim_exp,
    )


def _normal_ci(freq: float, n: int) -> tuple[float, float]:
    """Normal approximation 95% CI for a proportion."""
    se = math.sqrt(freq * (1 - freq) / n) if freq > 0 and freq < 1 else 0.0
    lo = max(0.0, freq - 1.96 * se)
    hi = min(1.0, freq + 1.96 * se)
    return lo, hi


def _expected_ci(idx: int, p0: float, n: int) -> tuple[float, float]:
    """95% CI for expected genotype frequencies under HW."""
    if idx == 0:  # AA
        se = math.sqrt(4 * p0**3 * (1 - p0) / (2 * n))
        freq = p0**2
    elif idx == 1:  # Aa
        se = math.sqrt(4 * p0 * (1 - p0) * (p0 + (1 - p0) - 4 * p0 * (1 - p0)) / (2 * n))
        freq = 2 * p0 * (1 - p0)
    else:  # aa
        se = math.sqrt(4 * (1 - p0) ** 3 * p0 / (2 * n))
        freq = (1 - p0) ** 2
    lo = max(0.0, freq - 1.96 * se)
    hi = min(1.0, freq + 1.96 * se)
    return lo, hi


def monte_carlo_multi_allele(
    data: MultiAlleleInput,
    n_simulations: int = 1000,
    seed: int | None = None,
) -> TestResult:
    """Monte Carlo exact probability estimation for k > 2 alleles.

    Translated from [SIMULATION] (lines 1369-1395) and [EXACTPROBCALC]
    (lines 1407-1415). Simulates random genotype configurations under
    the observed allele frequencies and compares exact multinomial
    probabilities.
    """
    rng = np.random.default_rng(seed)
    k = data.n_alleles
    n = data.n
    t = n_simulations
    freqs = data.allele_freqs

    # Pre-compute log-factorials
    max_val = 2 * n
    log_fac = np.zeros(max_val + 1)
    for i in range(1, max_val + 1):
        log_fac[i] = log_fac[i - 1] + math.log(i)

    nfac = log_fac[n]
    n2fac = log_fac[2 * n]
    constfac = nfac - n2fac

    # Cumulative frequency distribution for sampling
    cum_freqs = np.cumsum(freqs)

    def _exact_prob(genotype_matrix: np.ndarray, allele_counts: np.ndarray) -> float:
        """Compute exact multinomial probability for a genotype configuration."""
        allelfac = sum(log_fac[int(c)] for c in allele_counts)
        genotfac = 0.0
        hetlog = 0.0
        for i in range(k):
            for j in range(i, k):
                genotfac += log_fac[int(genotype_matrix[i, j])]
                if i != j:
                    hetlog += genotype_matrix[i, j] * math.log(2)
        return math.exp(constfac + allelfac - genotfac + hetlog)

    # Compute observed probability
    obs_genotypes = np.array(data.genotypes, dtype=float)
    obs_alleles = np.array(data.allele_counts, dtype=float)
    prob_obs = _exact_prob(obs_genotypes, obs_alleles)

    # Run simulations
    probt = 0
    for _ in range(t):
        sim_genotypes = np.zeros((k, k))
        sim_alleles = np.zeros(k)

        for _ in range(n):
            a_rand = rng.random()
            b_rand = rng.random()

            a_allele = 0
            for ai in range(k):
                if a_rand <= cum_freqs[ai]:
                    a_allele = ai
                    break

            b_allele = 0
            for bi in range(k):
                if b_rand <= cum_freqs[bi]:
                    b_allele = bi
                    break

            sim_alleles[a_allele] += 1
            sim_alleles[b_allele] += 1

            # Store in upper triangle
            i, j = min(a_allele, b_allele), max(a_allele, b_allele)
            sim_genotypes[i, j] += 1

        prob_sim = _exact_prob(sim_genotypes, sim_alleles)
        if prob_sim <= prob_obs:
            probt += 1

    exact_p_value = probt / t

    return TestResult(
        test_type=TestType.MONTE_CARLO,
        statistic=None,
        p_value=exact_p_value,
        df=None,
        label="Exact probability by Monte Carlo simulation (multi-allele)",
    )
