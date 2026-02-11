"""Shared fixtures for Hardy-Weinberg equilibrium tests.

Validation fixtures from the manual:
1. Two-allele: D=119, H=42, R=39 -> p=0.7, q=0.3
2. Four-allele: AA=2,AB=4,AC=6,AD=8,BB=10,BC=12,BD=14,CC=16,CD=18,DD=20
"""

from __future__ import annotations

import pytest

from hwtest.models import MultiAlleleInput, TwoAlleleInput
from hwtest.validators import validate_multi_allele, validate_two_allele


@pytest.fixture
def two_allele_data() -> TwoAlleleInput:
    """Standard two-allele test case from the HW_TEST manual.

    D=119 (AA), H=42 (Aa), R=39 (aa), N=200
    p = (2*119 + 42) / (2*200) = 280/400 = 0.7
    q = (42 + 2*39) / (2*200) = 120/400 = 0.3
    """
    return validate_two_allele(119, 42, 39)


@pytest.fixture
def four_allele_data() -> MultiAlleleInput:
    """Four-allele test case from the HW_TEST manual.

    Genotype matrix (upper triangle):
    AA=2,  AB=4,  AC=6,  AD=8
           BB=10, BC=12, BD=14
                  CC=16, CD=18
                         DD=20
    """
    genotypes = [
        [2, 4, 6, 8],
        [0, 10, 12, 14],
        [0, 0, 16, 18],
        [0, 0, 0, 20],
    ]
    return validate_multi_allele(genotypes, 4)


@pytest.fixture
def edge_case_d_zero() -> TwoAlleleInput:
    """Edge case: D=0 (no AA homozygotes)."""
    return validate_two_allele(0, 10, 5)


@pytest.fixture
def edge_case_r_zero() -> TwoAlleleInput:
    """Edge case: R=0 (no aa homozygotes)."""
    return validate_two_allele(5, 10, 0)


@pytest.fixture
def edge_case_small_n() -> TwoAlleleInput:
    """Edge case: minimal valid sample size."""
    return validate_two_allele(1, 1, 1)


@pytest.fixture
def edge_case_large_n() -> TwoAlleleInput:
    """Edge case: maximum population size."""
    return validate_two_allele(400, 200, 400)
