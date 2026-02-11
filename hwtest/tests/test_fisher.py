"""Tests for Fisher's exact test."""

from __future__ import annotations

from hwtest.models import TwoAlleleInput
from hwtest.stats.fisher import fisher_exact_test
from hwtest.validators import validate_two_allele


class TestFisherExact:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result = fisher_exact_test(two_allele_data)
        assert result.p_value is not None
        assert result.p_value < 1e-6

    def test_undefined_d_zero_h_one(self) -> None:
        """Fisher's test is undefined when D=0 and H=1."""
        data = validate_two_allele(0, 1, 5)
        result = fisher_exact_test(data)
        assert result.p_value is None

    def test_undefined_r_zero_h_one(self) -> None:
        """Fisher's test is undefined when R=0 and H=1."""
        data = validate_two_allele(5, 1, 0)
        result = fisher_exact_test(data)
        assert result.p_value is None

    def test_valid_p_range(self) -> None:
        """P-value should be between 0 and 1."""
        data = validate_two_allele(10, 20, 10)
        result = fisher_exact_test(data)
        assert result.p_value is not None
        assert 0 <= result.p_value <= 1

    def test_hw_equilibrium_sample(self) -> None:
        """A sample near HW equilibrium should have a large p-value."""
        # p=0.5 -> expected D=25, H=50, R=25
        data = validate_two_allele(25, 50, 25)
        result = fisher_exact_test(data)
        assert result.p_value is not None
        assert result.p_value > 0.05

    def test_edge_d_zero(self, edge_case_d_zero: TwoAlleleInput) -> None:
        result = fisher_exact_test(edge_case_d_zero)
        assert result.p_value is not None

    def test_edge_r_zero(self, edge_case_r_zero: TwoAlleleInput) -> None:
        result = fisher_exact_test(edge_case_r_zero)
        assert result.p_value is not None
