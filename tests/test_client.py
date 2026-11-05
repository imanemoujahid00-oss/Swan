from unittest.mock import Mock, patch
import pytest
import requests
from swan_ui.client import RecommendationUnavailable, fetch_recommendations
from swan_ui.profile import Profile


def test_unavailable_api_never_returns_products():
    profile = Profile(True, "acne_prone", 2, (), "oily", "no", ())
    with patch("swan_ui.client.requests.post", side_effect=requests.Timeout):
        with pytest.raises(RecommendationUnavailable):
            fetch_recommendations(profile)


def test_cloudrun_client_uses_service_identity():
    profile = Profile(True, "acne_prone", 2, (), "oily", "no", ())
    identity = Mock(status_code=200, text="short-lived-test-token")
    response = Mock()
    response.json.return_value = {"status": "ok", "results": []}
    with patch.dict("os.environ", {"SWAN_API_AUTH": "cloudrun", "SWAN_API_URL": "https://private-api.example"}):
        with patch("swan_ui.client.requests.get", return_value=identity) as get:
            with patch("swan_ui.client.requests.post", return_value=response) as post:
                fetch_recommendations(profile)
    assert get.call_args.kwargs["params"] == {"audience": "https://private-api.example"}
    assert post.call_args.kwargs["headers"] == {"Authorization": "Bearer short-lived-test-token"}


def test_failed_service_identity_never_sends_profile_to_api():
    profile = Profile(True, "acne_prone", 2, (), "oily", "no", ())
    with patch.dict("os.environ", {"SWAN_API_AUTH": "cloudrun"}):
        with patch("swan_ui.client.requests.get", side_effect=requests.Timeout):
            with patch("swan_ui.client.requests.post") as post:
                with pytest.raises(RecommendationUnavailable):
                    fetch_recommendations(profile)
                post.assert_not_called()
