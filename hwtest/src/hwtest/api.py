"""FastAPI backend for Hardy-Weinberg equilibrium testing."""

from __future__ import annotations

from typing import Any

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
except ImportError as e:
    raise ImportError(
        "API dependencies not installed. Install with: pip install hwtest[api]"
    ) from e

from hwtest.engine import run_multi_allele, run_two_allele
from hwtest.models import TestType
from hwtest.validators import ValidationError, validate_multi_allele, validate_two_allele

app = FastAPI(
    title="HW_TEST API",
    description="Hardy-Weinberg Equilibrium Testing (Santos, Lemes & Otto, 2020)",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TwoAlleleRequest(BaseModel):
    d: int
    h: int
    r: int
    tests: list[str] | None = None
    seed: int | None = None
    simulations: int = 1000


class MultiAlleleRequest(BaseModel):
    genotypes: list[list[int]]
    n_alleles: int
    tests: list[str] | None = None
    seed: int | None = None
    simulations: int = 1000


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/test")
def run_test(request: TwoAlleleRequest | MultiAlleleRequest) -> dict[str, Any]:
    """Run Hardy-Weinberg equilibrium tests."""
    try:
        if isinstance(request, TwoAlleleRequest):
            data = validate_two_allele(request.d, request.h, request.r)
            test_set = _parse_tests(request.tests) if request.tests else None
            results = run_two_allele(
                data, tests=test_set, mc_seed=request.seed, mc_simulations=request.simulations
            )
            return {
                "type": "two_allele",
                "n": data.n,
                "d": data.d,
                "h": data.h,
                "r": data.r,
                "p_freq": results.p_freq,
                "q_freq": results.q_freq,
                "test_results": [
                    {
                        "test": tr.test_type.value,
                        "label": tr.label,
                        "statistic": tr.statistic,
                        "p_value": tr.p_value,
                        "df": tr.df,
                    }
                    for tr in results.test_results
                ],
            }
        else:
            data = validate_multi_allele(request.genotypes, request.n_alleles)
            test_set = _parse_tests(request.tests) if request.tests else None
            results = run_multi_allele(
                data, tests=test_set, mc_seed=request.seed, mc_simulations=request.simulations
            )
            return {
                "type": "multi_allele",
                "allele_freqs": results.allele_freqs,
                "test_results": [
                    {
                        "test": tr.test_type.value,
                        "label": tr.label,
                        "statistic": tr.statistic,
                        "p_value": tr.p_value,
                        "df": tr.df,
                    }
                    for tr in results.test_results
                ],
            }
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


def _parse_tests(test_names: list[str]) -> set[TestType]:
    result = set()
    for name in test_names:
        try:
            result.add(TestType(name))
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"Unknown test '{name}'. Valid: {[t.value for t in TestType]}",
            )
    return result
