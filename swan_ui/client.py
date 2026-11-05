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
        headers = {}
        if os.environ.get("SWAN_API_AUTH") == "cloudrun":
            # Cloud Run supplies a short-lived identity token; no key file is stored.
            identity = requests.get(
                "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity",
                params={"audience": base_url},
                headers={"Metadata-Flavor": "Google"}, timeout=(2, 5),
                allow_redirects=False,
            )
            identity.raise_for_status()
            token = identity.text.strip()
            if not token or identity.status_code != 200:
                raise ValueError("Service identity unavailable")
            headers["Authorization"] = "Bearer " + token
        response = requests.post(base_url + "/v1/recommendations", json=payload,
                                 headers=headers, timeout=(5, 60))
        response.raise_for_status()
        body = response.json()
        if not isinstance(body, dict) or not isinstance(body.get("results"), list):
            raise ValueError("Invalid API response")
        return body
    except (requests.RequestException, ValueError) as exc:
        raise RecommendationUnavailable("Recommendations are temporarily unavailable. Please try again.") from exc
