"""Integration tests for the engine orchestrator."""

from __future__ import annotations

from hwtest.engine import run_multi_allele, run_two_allele
from hwtest.models import TestType, TwoAlleleInput


class TestRunTwoAllele:
    def test_all_tests(self, two_allele_data: TwoAlleleInput) -> None:
        results = run_two_allele(two_allele_data, mc_seed=42)
        assert len(results.test_results) == 9
        for tr in results.test_results:
            if tr.test_type != TestType.FISHER_EXACT:
                assert tr.p_value is not None

    def test_selected_tests(self, two_allele_data: TwoAlleleInput) -> None:
        tests = {TestType.CHI_SQUARE, TestType.HALDANE_EXACT}
        results = run_two_allele(two_allele_data, tests=tests)
        assert len(results.test_results) == 2

    def test_expected_frequencies(self, two_allele_data: TwoAlleleInput) -> None:
        results = run_two_allele(two_allele_data)
        ef = results.expected_frequencies
        # Sum of expected should equal N
        assert abs(sum(ef.no_correction) - two_allele_data.n) < 0.001
        assert abs(sum(ef.hogben_levene) - two_allele_data.n) < 0.001

    def test_allele_frequencies(self, two_allele_data: TwoAlleleInput) -> None:
        results = run_two_allele(two_allele_data)
        assert abs(results.p_freq - 0.7) < 0.001
        assert abs(results.q_freq - 0.3) < 0.001

    def test_bootstrap_only_with_mc(self, two_allele_data: TwoAlleleInput) -> None:
        results = run_two_allele(
            two_allele_data,
            tests={TestType.CHI_SQUARE},
        )
        assert results.bootstrap is None

    def test_bootstrap_present_with_mc(self, two_allele_data: TwoAlleleInput) -> None:
        results = run_two_allele(
            two_allele_data,
            tests={TestType.MONTE_CARLO},
            mc_seed=42,
        )
        assert results.bootstrap is not None


class TestRunMultiAllele:
    def test_chi_square_only(self, four_allele_data) -> None:
        results = run_multi_allele(
            four_allele_data, tests={TestType.CHI_SQUARE}
        )
        assert len(results.test_results) == 1
        assert results.test_results[0].test_type == TestType.CHI_SQUARE

    def test_unsupported_test_filtered(self, four_allele_data) -> None:
        """Multi-allele should filter out unsupported tests silently."""
        results = run_multi_allele(
            four_allele_data,
            tests={TestType.CHI_SQUARE, TestType.FISHER_EXACT},
        )
        # Fisher is not supported for multi-allele
        assert len(results.test_results) == 1

    def test_allele_frequencies(self, four_allele_data) -> None:
        results = run_multi_allele(four_allele_data)
        assert len(results.allele_freqs) == 4
        assert abs(sum(results.allele_freqs) - 1.0) < 0.001
