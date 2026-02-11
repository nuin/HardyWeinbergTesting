"""Tests for input validation."""

from __future__ import annotations

import pytest

from hwtest.validators import ValidationError, validate_multi_allele, validate_two_allele


class TestValidateTwoAllele:
    def test_valid_input(self) -> None:
        data = validate_two_allele(119, 42, 39)
        assert data.d == 119
        assert data.h == 42
        assert data.r == 39
        assert data.n == 200

    def test_negative_count(self) -> None:
        with pytest.raises(ValidationError, match="non-negative"):
            validate_two_allele(-1, 10, 5)

    def test_n_too_small(self) -> None:
        with pytest.raises(ValidationError, match="too small"):
            validate_two_allele(1, 0, 0)

    def test_n_too_large(self) -> None:
        with pytest.raises(ValidationError, match="exceeds maximum"):
            validate_two_allele(500, 500, 500)

    def test_p_zero(self) -> None:
        """All alleles must be present."""
        with pytest.raises(ValidationError, match="Both alleles"):
            validate_two_allele(0, 0, 10)

    def test_q_zero(self) -> None:
        with pytest.raises(ValidationError, match="Both alleles"):
            validate_two_allele(10, 0, 0)

    def test_minimum_valid(self) -> None:
        data = validate_two_allele(1, 1, 1)
        assert data.n == 3


class TestValidateMultiAllele:
    def test_valid_input(self) -> None:
        genotypes = [
            [2, 4, 6, 8],
            [0, 10, 12, 14],
            [0, 0, 16, 18],
            [0, 0, 0, 20],
        ]
        data = validate_multi_allele(genotypes, 4)
        assert data.n_alleles == 4
        assert data.n == 110

    def test_allele_count_too_low(self) -> None:
        with pytest.raises(ValidationError, match="between 3 and 12"):
            validate_multi_allele([[1]], 1)

    def test_allele_count_too_high(self) -> None:
        genotypes = [[0] * 13 for _ in range(13)]
        with pytest.raises(ValidationError, match="between 3 and 12"):
            validate_multi_allele(genotypes, 13)

    def test_negative_count(self) -> None:
        genotypes = [
            [-1, 4, 6],
            [0, 10, 12],
            [0, 0, 16],
        ]
        with pytest.raises(ValidationError, match="negative"):
            validate_multi_allele(genotypes, 3)

    def test_zero_allele_frequency(self) -> None:
        genotypes = [
            [0, 0, 10],
            [0, 0, 0],
            [0, 0, 10],
        ]
        with pytest.raises(ValidationError, match="zero frequency"):
            validate_multi_allele(genotypes, 3)

    def test_row_length_mismatch(self) -> None:
        genotypes = [
            [2, 4, 6],
            [0, 10],
            [0, 0, 16],
        ]
        with pytest.raises(ValidationError, match="columns"):
            validate_multi_allele(genotypes, 3)
