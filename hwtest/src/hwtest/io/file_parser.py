"""Parse input files for Hardy-Weinberg equilibrium testing.

Supports comma-separated .txt files matching the original program's format.
"""

from __future__ import annotations

from pathlib import Path

from hwtest.models import MultiAlleleInput, TwoAlleleInput
from hwtest.validators import validate_multi_allele, validate_two_allele


def parse_two_allele_file(path: str | Path) -> TwoAlleleInput:
    """Parse a two-allele input file.

    Expected format: three comma-separated integers (D, H, R) on one line
    or three lines with one integer each.
    """
    text = Path(path).read_text().strip()

    if "," in text:
        parts = [p.strip() for p in text.split(",")]
    else:
        parts = text.split()

    if len(parts) != 3:
        raise ValueError(
            f"Expected 3 values (D, H, R), got {len(parts)}. "
            f"File content: {text!r}"
        )

    d, h, r = int(parts[0]), int(parts[1]), int(parts[2])
    return validate_two_allele(d, h, r)


def parse_multi_allele_file(path: str | Path, n_alleles: int) -> MultiAlleleInput:
    """Parse a multi-allele input file.

    Expected format: comma-separated integers representing the upper
    triangle of the genotype matrix, read row by row.
    For k alleles, there are k(k+1)/2 values.
    """
    text = Path(path).read_text().strip()

    if "," in text:
        parts = [p.strip() for p in text.split(",")]
    else:
        parts = text.split()

    n_expected = n_alleles * (n_alleles + 1) // 2
    if len(parts) != n_expected:
        raise ValueError(
            f"Expected {n_expected} values for {n_alleles} alleles, "
            f"got {len(parts)}."
        )

    values = [int(p) for p in parts]

    # Fill upper-triangular matrix
    genotypes = [[0] * n_alleles for _ in range(n_alleles)]
    idx = 0
    for i in range(n_alleles):
        for j in range(i, n_alleles):
            genotypes[i][j] = values[idx]
            idx += 1

    return validate_multi_allele(genotypes, n_alleles)


def parse_data_string(data_str: str, n_alleles: int) -> TwoAlleleInput | MultiAlleleInput:
    """Parse a comma-separated data string (from CLI --data flag)."""
    parts = [p.strip() for p in data_str.split(",")]
    values = [int(p) for p in parts]

    if n_alleles == 2:
        if len(values) != 3:
            raise ValueError(f"Two-allele input requires 3 values (D,H,R), got {len(values)}.")
        return validate_two_allele(values[0], values[1], values[2])

    n_expected = n_alleles * (n_alleles + 1) // 2
    if len(values) != n_expected:
        raise ValueError(
            f"Expected {n_expected} values for {n_alleles} alleles, got {len(values)}."
        )

    genotypes = [[0] * n_alleles for _ in range(n_alleles)]
    idx = 0
    for i in range(n_alleles):
        for j in range(i, n_alleles):
            genotypes[i][j] = values[idx]
            idx += 1

    return validate_multi_allele(genotypes, n_alleles)
