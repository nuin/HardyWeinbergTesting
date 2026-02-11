"""Tests for G-test (log-likelihood ratio test)."""

from __future__ import annotations

from hwtest.models import TwoAlleleInput
from hwtest.stats.g_test import g_test_corrected, g_test_no_correction


class TestGTestNoCorrection:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result = g_test_no_correction(two_allele_data)
        assert result.statistic is not None
        assert result.statistic > 0
        assert result.p_value is not None
        assert result.p_value < 1e-6

    def test_edge_d_zero(self, edge_case_d_zero: TwoAlleleInput) -> None:
        result = g_test_no_correction(edge_case_d_zero)
        assert result.statistic is not None
        assert result.p_value is not None

    def test_edge_r_zero(self, edge_case_r_zero: TwoAlleleInput) -> None:
        result = g_test_no_correction(edge_case_r_zero)
        assert result.statistic is not None
        assert result.p_value is not None


class TestGTestCorrected:
    def test_standard_case(self, two_allele_data: TwoAlleleInput) -> None:
        result = g_test_corrected(two_allele_data)
        assert result.statistic is not None
        assert result.p_value is not None
        assert result.p_value < 1e-6

    def test_edge_d_zero(self, edge_case_d_zero: TwoAlleleInput) -> None:
        result = g_test_corrected(edge_case_d_zero)
        assert result.statistic is not None

    def test_edge_r_zero(self, edge_case_r_zero: TwoAlleleInput) -> None:
        result = g_test_corrected(edge_case_r_zero)
        assert result.statistic is not None
