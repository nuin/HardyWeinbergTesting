"""Tests for chi-square variants."""

from __future__ import annotations

import pytest

from hwtest.models import TwoAlleleInput
from hwtest.stats.chi_square import (
    chi_square_cannings_edwards,
    chi_square_hogben_levene,
    chi_square_multi_allele,
    chi_square_no_correction,
    chi_square_yates,
)


class TestChiSquareNoCorrection:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result = chi_square_no_correction(two_allele_data)
        assert result.statistic is not None
        assert result.statistic > 0
        assert result.p_value is not None
        # D=119, H=42, R=39: strong departure from HWE
        assert result.p_value < 1e-6
        assert result.df == 1

    def test_formula_values(self) -> None:
        """Verify chi-square formula: N*(H^2 - 4DR)^2 / (PQ)^2."""
        from hwtest.validators import validate_two_allele

        data = validate_two_allele(119, 42, 39)
        result = chi_square_no_correction(data)
        # Manual calc: N=200, H=42, D=119, R=39
        # H^2 - 4DR = 1764 - 18564 = -16800
        # P = 280, Q = 120
        # chi2 = 200 * 16800^2 / (280*120)^2
        expected_chi2 = 200 * (42 * 42 - 4 * 119 * 39) ** 2 / (280 * 120) ** 2
        assert abs(result.statistic - expected_chi2) < 1e-10  # type: ignore[operator]

    def test_edge_d_zero(self, edge_case_d_zero: TwoAlleleInput) -> None:
        result = chi_square_no_correction(edge_case_d_zero)
        assert result.statistic is not None
        assert result.p_value is not None

    def test_edge_r_zero(self, edge_case_r_zero: TwoAlleleInput) -> None:
        result = chi_square_no_correction(edge_case_r_zero)
        assert result.statistic is not None
        assert result.p_value is not None


class TestChiSquareYates:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result = chi_square_yates(two_allele_data)
        assert result.p_value is not None
        assert result.p_value < 1e-6

    def test_less_than_uncorrected(self, two_allele_data: TwoAlleleInput) -> None:
        """Yates' correction should produce a smaller or equal chi-square."""
        uncorrected = chi_square_no_correction(two_allele_data)
        corrected = chi_square_yates(two_allele_data)
        assert corrected.statistic <= uncorrected.statistic  # type: ignore[operator]


class TestChiSquareHogbenLevene:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result = chi_square_hogben_levene(two_allele_data)
        assert result.p_value is not None
        assert result.p_value < 1e-6

    def test_edge_small(self, edge_case_small_n: TwoAlleleInput) -> None:
        result = chi_square_hogben_levene(edge_case_small_n)
        assert result.statistic is not None


class TestChiSquareCanningsEdwards:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result = chi_square_cannings_edwards(two_allele_data)
        assert result.p_value is not None
        assert result.p_value < 1e-6


class TestChiSquareMultiAllele:
    def test_four_allele(self, four_allele_data) -> None:
        result = chi_square_multi_allele(four_allele_data)
        assert result.statistic is not None
        assert result.df == 6  # k*(k-1)/2 = 4*3/2 = 6
        assert result.p_value is not None
        # From manual: p = 0.0465
        assert abs(result.p_value - 0.0465) < 0.01
