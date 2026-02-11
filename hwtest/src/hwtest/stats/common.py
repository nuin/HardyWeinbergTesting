"""Common utilities for statistical calculations."""

from __future__ import annotations

from hwtest.models import MultiAlleleInput, TwoAlleleInput


def allele_frequencies_two(data: TwoAlleleInput) -> tuple[float, float]:
    """Calculate allele frequencies p and q for a two-allele system."""
    return data.p_freq, data.q_freq


def allele_frequencies_multi(data: MultiAlleleInput) -> list[float]:
    """Calculate allele frequencies for a multi-allele system."""
    return data.allele_freqs
