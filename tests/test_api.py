from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from api.main import create_app

ROOT = Path(__file__).resolve().parents[1]
BASE = {"is_adult": True, "concern": "acne_prone", "blemish_level": 2, "referral_flags": [], "skin_type": "oily", "reactivity": False, "avoid": []}


def test_api_serves_real_ranker_and_excludes_aroma():
    with TestClient(create_app(ROOT / "raw_data")) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/ready").json()["products"] == 50
        result = client.post("/v1/recommendations", json=BASE | {"avoid": ["fragrance"]})
        assert result.status_code == 200
        body = result.json()
        assert body["status"] == "ok"
        assert len(body["results"]) == 3
        assert "3515450016527" not in [p["code"] for p in body["results"]]
        assert all(isinstance(p["code"], str) and p["reason"] for p in body["results"])
        assert body["catalogue_version"]


@pytest.mark.parametrize("changes,status", [
    ({"is_adult": False}, "referral"), ({"concern": "other"}, "out_of_scope"),
    ({"concern": "dryness_barrier"}, "coming_soon"), ({"concern": "sensitivity"}, "coming_soon"),
    ({"blemish_level": 4}, "referral"), ({"blemish_level": 5}, "referral"),
    ({"blemish_level": None}, "incomplete_profile"), ({"blemish_level": 0}, "incomplete_profile"),
    ({"referral_flags": ["prescribed_treatment"]}, "referral"),
])
def test_routes_without_catalogue(tmp_path, changes, status):
    with TestClient(create_app(tmp_path)) as client:
        result = client.post("/v1/recommendations", json=BASE | changes)
        assert result.json()["status"] == status
        assert result.json()["results"] == []
        assert result.json()["message"]


def test_missing_data_is_unavailable_not_sample_products(tmp_path):
    with TestClient(create_app(tmp_path)) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/ready").status_code == 503
        result = client.post("/v1/recommendations", json=BASE)
        assert result.status_code == 503
        assert result.json()["error"]["code"] == "model_unavailable"


@pytest.mark.parametrize("value", ["2", True, 2.5])
def test_rejects_wrong_blemish_types_without_echoing_profile(value):
    with TestClient(create_app()) as client:
        result = client.post("/v1/recommendations", json=BASE | {"blemish_level": value})
        assert result.status_code == 422
        assert "input" not in result.text
