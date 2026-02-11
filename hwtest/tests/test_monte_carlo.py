"""Tests for Monte Carlo simulation."""

from __future__ import annotations

from hwtest.models import TwoAlleleInput
from hwtest.stats.monte_carlo import monte_carlo_multi_allele, monte_carlo_two_allele
from hwtest.validators import validate_two_allele


class TestMonteCarloTwoAllele:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result, bootstrap = monte_carlo_two_allele(two_allele_data, seed=42)
        assert result.p_value is not None
        # Strong departure: p-value should be very small
        assert result.p_value < 0.05

    def test_reproducibility(self, two_allele_data: TwoAlleleInput) -> None:
        """Same seed should produce same result."""
        r1, _ = monte_carlo_two_allele(two_allele_data, seed=42)
        r2, _ = monte_carlo_two_allele(two_allele_data, seed=42)
        assert r1.p_value == r2.p_value

    def test_hw_equilibrium(self) -> None:
        """A sample near HW equilibrium should have a large p-value."""
        data = validate_two_allele(25, 50, 25)
        result, bootstrap = monte_carlo_two_allele(data, seed=42)
        assert result.p_value is not None
        # Tolerant: MC is stochastic
        assert result.p_value > 0.01

    def test_bootstrap_estimates(self, two_allele_data: TwoAlleleInput) -> None:
        _, bootstrap = monte_carlo_two_allele(two_allele_data, seed=42)
        assert len(bootstrap.observed) == 3  # AA, Aa, aa
        assert len(bootstrap.expected) == 3
        assert len(bootstrap.sim_points_observed) == 1000
        assert len(bootstrap.sim_points_expected) == 1000

    def test_edge_d_zero(self, edge_case_d_zero: TwoAlleleInput) -> None:
        result, _ = monte_carlo_two_allele(edge_case_d_zero, seed=42)
        assert result.p_value is not None


class TestMonteCarloMultiAllele:
    def test_four_allele(self, four_allele_data) -> None:
        result = monte_carlo_multi_allele(four_allele_data, seed=42)
        assert result.p_value is not None
        assert 0 <= result.p_value <= 1

    def test_reproducibility(self, four_allele_data) -> None:
        r1 = monte_carlo_multi_allele(four_allele_data, seed=42)
        r2 = monte_carlo_multi_allele(four_allele_data, seed=42)
        assert r1.p_value == r2.p_value
