"""Tests for the FastAPI backend."""

from __future__ import annotations

import pytest


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        pytest.skip("FastAPI not installed")

    from hwtest.api import app
    return TestClient(app)


class TestHealthEndpoint:
    def test_health(self, client) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestTwoAlleleEndpoint:
    def test_basic_request(self, client) -> None:
        response = client.post("/api/test", json={
            "d": 119, "h": 42, "r": 39,
        })
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "two_allele"
        assert abs(data["p_freq"] - 0.7) < 0.001

    def test_selected_tests(self, client) -> None:
        response = client.post("/api/test", json={
            "d": 119, "h": 42, "r": 39,
            "tests": ["chi_square", "haldane_exact"],
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["test_results"]) == 2

    def test_invalid_data(self, client) -> None:
        response = client.post("/api/test", json={
            "d": -1, "h": 42, "r": 39,
        })
        assert response.status_code == 422


class TestMultiAlleleEndpoint:
    def test_four_allele(self, client) -> None:
        response = client.post("/api/test", json={
            "genotypes": [
                [2, 4, 6, 8],
                [0, 10, 12, 14],
                [0, 0, 16, 18],
                [0, 0, 0, 20],
            ],
            "n_alleles": 4,
        })
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "multi_allele"
        assert len(data["allele_freqs"]) == 4
