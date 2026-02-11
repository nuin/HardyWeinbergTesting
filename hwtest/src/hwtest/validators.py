"""Input validation for Hardy-Weinberg equilibrium testing."""

from __future__ import annotations

from hwtest.models import MultiAlleleInput, TwoAlleleInput


class ValidationError(Exception):
    """Raised when input data fails validation."""


def validate_two_allele(d: int, h: int, r: int) -> TwoAlleleInput:
    """Validate and create a TwoAlleleInput.

    Constraints (from original program):
    - D, H, R >= 0
    - N = D + H + R, with N <= 1000
    - P = 2D + H > 0 and Q = H + 2R > 0 (both alleles present)
    - N >= 3
    """
    if d < 0 or h < 0 or r < 0:
        raise ValidationError("Genotype counts must be non-negative.")

    n = d + h + r
    if n < 3:
        raise ValidationError(f"Sample size N={n} is too small. Minimum is 3.")

    if n > 1000:
        raise ValidationError(f"Sample size N={n} exceeds maximum of 1000.")

    p = 2 * d + h
    q = h + 2 * r
    if p == 0 or q == 0:
        raise ValidationError(
            "Both alleles must be present in the sample (P > 0 and Q > 0)."
        )

    return TwoAlleleInput(d=d, h=h, r=r)


def validate_multi_allele(
    genotypes: list[list[int]], n_alleles: int
) -> MultiAlleleInput:
    """Validate and create a MultiAlleleInput.

    genotypes is an upper-triangular matrix: genotypes[i][j] for i <= j.
    """
    if n_alleles < 3 or n_alleles > 12:
        raise ValidationError(
            f"Number of alleles must be between 3 and 12, got {n_alleles}."
        )

    if len(genotypes) != n_alleles:
        raise ValidationError(
            f"Genotype matrix has {len(genotypes)} rows, expected {n_alleles}."
        )

    for i, row in enumerate(genotypes):
        if len(row) != n_alleles:
            raise ValidationError(
                f"Genotype matrix row {i} has {len(row)} columns, expected {n_alleles}."
            )
        for j in range(i, n_alleles):
            if row[j] < 0:
                raise ValidationError(
                    f"Genotype count at ({i},{j}) is negative: {row[j]}."
                )

    data = MultiAlleleInput(genotypes=genotypes, n_alleles=n_alleles)

    if data.n > 1000:
        raise ValidationError(
            f"Sample size N={data.n} exceeds maximum of 1000."
        )

    if data.n < 3:
        raise ValidationError(
            f"Sample size N={data.n} is too small. Minimum is 3."
        )

    # Check that all alleles are present
    freqs = data.allele_freqs
    for i, f in enumerate(freqs):
        if f == 0.0:
            raise ValidationError(
                f"Allele {chr(65 + i)} has zero frequency. "
                f"This locus has fewer than {n_alleles} alleles."
            )

    return data
