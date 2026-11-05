"""API-only recommendation client. Never return sample products on failure."""
from dataclasses import asdict
import os
import requests


class RecommendationUnavailable(RuntimeError):
    pass


def fetch_recommendations(profile):
    payload = asdict(profile)
    payload["reactivity"] = {"yes": True, "no": False, "not_sure": None}[profile.reactivity]
    base_url = os.environ.get("SWAN_API_URL", "http://127.0.0.1:8000").rstrip("/")
    try:
        response = requests.post(base_url + "/v1/recommendations", json=payload, timeout=(5, 20))
        response.raise_for_status()
        body = response.json()
        if not isinstance(body, dict) or not isinstance(body.get("results"), list):
            raise ValueError("Invalid API response")
        return body
    except (requests.RequestException, ValueError) as exc:
        raise RecommendationUnavailable("Recommendations are temporarily unavailable. Please try again.") from exc
