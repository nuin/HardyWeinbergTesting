"""Data models for Hardy-Weinberg equilibrium testing."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TestType(str, Enum):
    """Available statistical tests for HW equilibrium."""

    CHI_SQUARE = "chi_square"
    CHI_SQUARE_YATES = "chi_square_yates"
    CHI_SQUARE_HOGBEN_LEVENE = "chi_square_hogben_levene"
    CHI_SQUARE_CANNINGS_EDWARDS = "chi_square_cannings_edwards"
    G_TEST = "g_test"
    G_TEST_CORRECTED = "g_test_corrected"
    FISHER_EXACT = "fisher_exact"
    HALDANE_EXACT = "haldane_exact"
    MONTE_CARLO = "monte_carlo"


# Tests available for multi-allele (k > 2) case
MULTI_ALLELE_TESTS = {TestType.CHI_SQUARE, TestType.MONTE_CARLO}

ALL_TWO_ALLELE_TESTS = set(TestType)


@dataclass(frozen=True)
class TwoAlleleInput:
    """Input data for a two-allele Hardy-Weinberg test.

    D = count of AA homozygotes
    H = count of Aa heterozygotes
    R = count of aa homozygotes
    """

    d: int  # N(AA)
    h: int  # N(Aa)
    r: int  # N(aa)

    @property
    def n(self) -> int:
        return self.d + self.h + self.r

    @property
    def p_count(self) -> int:
        """Allele count for A: 2D + H."""
        return 2 * self.d + self.h

    @property
    def q_count(self) -> int:
        """Allele count for a: H + 2R."""
        return self.h + 2 * self.r

    @property
    def p_freq(self) -> float:
        """Allele frequency p = P(A)."""
        return self.p_count / (2 * self.n)

    @property
    def q_freq(self) -> float:
        """Allele frequency q = P(a)."""
        return self.q_count / (2 * self.n)


@dataclass(frozen=True)
class MultiAlleleInput:
    """Input data for a multi-allele (k > 2) Hardy-Weinberg test.

    genotypes: upper-triangular matrix where genotypes[i][j] = count of
    genotype (allele_i, allele_j) with i <= j.
    n_alleles: number of alleles (3-12).
    """

    genotypes: list[list[int]]
    n_alleles: int

    @property
    def n(self) -> int:
        """Total number of individuals."""
        total = 0
        for i in range(self.n_alleles):
            for j in range(i, self.n_alleles):
                total += self.genotypes[i][j]
        return total

    @property
    def allele_counts(self) -> list[int]:
        """Count of each allele across all genotypes."""
        counts = [0] * self.n_alleles
        for i in range(self.n_alleles):
            for j in range(i, self.n_alleles):
                counts[i] += self.genotypes[i][j]
                counts[j] += self.genotypes[i][j]
        return counts

    @property
    def allele_freqs(self) -> list[float]:
        """Frequency of each allele."""
        two_n = 2 * self.n
        return [c / two_n for c in self.allele_counts]


@dataclass
class TestResult:
    """Result of a single statistical test."""

    test_type: TestType
    statistic: float | None = None
    p_value: float | None = None
    df: int | None = None
    label: str = ""


@dataclass
class ExpectedFrequencies:
    """Expected genotype frequencies under different corrections."""

    no_correction: tuple[float, float, float] = (0.0, 0.0, 0.0)
    hogben_levene: tuple[float, float, float] = (0.0, 0.0, 0.0)
    cannings_edwards: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class BootstrapEstimates:
    """Bootstrap simulation estimates for genotype frequencies."""

    mean_p: float = 0.0
    observed: list[GenotypeBootstrap] = field(default_factory=list)
    expected: list[GenotypeBootstrap] = field(default_factory=list)
    exact_p_value: float = 0.0
    sim_points_observed: list[tuple[float, float]] = field(default_factory=list)
    sim_points_expected: list[tuple[float, float]] = field(default_factory=list)


@dataclass
class GenotypeBootstrap:
    """Bootstrap estimates for a single genotype."""

    genotype_label: str
    observed_freq: float
    normal_ci: tuple[float, float]
    bootstrap_mean: float
    bootstrap_median: float
    bootstrap_ci: tuple[float, float]


@dataclass
class TwoAlleleResults:
    """Complete results for a two-allele HW test."""

    input_data: TwoAlleleInput
    expected_frequencies: ExpectedFrequencies
    p_freq: float
    q_freq: float
    se_h0: float  # s.e. under H0
    se_h1: float  # s.e. under H1 (HW equilibrium)
    test_results: list[TestResult] = field(default_factory=list)
    bootstrap: BootstrapEstimates | None = None


@dataclass
class MultiAlleleResults:
    """Complete results for a multi-allele HW test."""

    input_data: MultiAlleleInput
    allele_freqs: list[float] = field(default_factory=list)
    test_results: list[TestResult] = field(default_factory=list)
    bootstrap: BootstrapEstimates | None = None
