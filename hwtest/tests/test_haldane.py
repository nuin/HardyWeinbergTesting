"""Tests for Haldane's exact test."""

from __future__ import annotations

from hwtest.models import TwoAlleleInput
from hwtest.stats.haldane import haldane_exact_test
from hwtest.validators import validate_two_allele


class TestHaldaneExact:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result = haldane_exact_test(two_allele_data)
        assert result.p_value is not None
        assert result.p_value < 1e-6

    def test_valid_p_range(self) -> None:
        data = validate_two_allele(10, 20, 10)
        result = haldane_exact_test(data)
        assert result.p_value is not None
        assert 0 <= result.p_value <= 1

    def test_hw_equilibrium_sample(self) -> None:
        """A sample near HW equilibrium should have a large p-value."""
        data = validate_two_allele(25, 50, 25)
        result = haldane_exact_test(data)
        assert result.p_value is not None
        assert result.p_value > 0.05

    def test_edge_even_h(self) -> None:
        """Even H: HMIN = 0."""
        data = validate_two_allele(5, 10, 5)
        result = haldane_exact_test(data)
        assert result.p_value is not None

    def test_edge_odd_h(self) -> None:
        """Odd H: HMIN = 1."""
        data = validate_two_allele(5, 11, 5)
        result = haldane_exact_test(data)
        assert result.p_value is not None

    def test_edge_d_zero(self, edge_case_d_zero: TwoAlleleInput) -> None:
        result = haldane_exact_test(edge_case_d_zero)
        assert result.p_value is not None

    def test_edge_r_zero(self, edge_case_r_zero: TwoAlleleInput) -> None:
        result = haldane_exact_test(edge_case_r_zero)
        assert result.p_value is not None
