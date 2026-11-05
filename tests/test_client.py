from unittest.mock import patch
import pytest
import requests
from swan_ui.client import RecommendationUnavailable, fetch_recommendations
from swan_ui.profile import Profile


def test_unavailable_api_never_returns_products():
    profile = Profile(True, "acne_prone", 2, (), "oily", "no", ())
    with patch("swan_ui.client.requests.post", side_effect=requests.Timeout):
        with pytest.raises(RecommendationUnavailable):
            fetch_recommendations(profile)
