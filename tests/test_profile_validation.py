"""Routing regression checks; no catalogue or scoring data required."""

import importlib.util
from pathlib import Path
import sys
import types
import unittest
import numpy as np
from unittest.mock import Mock, patch


class ProfileValidationTests(unittest.TestCase):
    def setUp(self):
        baseline = types.ModuleType("models.baseline")
        baseline.rank_moisturizers = Mock(
            side_effect=AssertionError("Invalid profiles must not reach ranking")
        )
        spec = importlib.util.spec_from_file_location(
            "recommendations_under_test",
            Path(__file__).resolve().parents[1] / "models/recommendations.py",
        )
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"models.baseline": baseline}):
            spec.loader.exec_module(self.module)
        self.profile = {
            "is_adult": True, "concern": "acne_prone", "blemish_level": 2,
            "referral_flags": [], "skin_type": "oily", "reactivity": False,
            "avoid": [],
        }

    def test_invalid_blemish_levels_return_incomplete_profile(self):
        for value in (None, "2", 0, 6, -1, True, 2.0, [], {}):
            with self.subTest(value=value):
                result = self.module.recommend(
                    self.profile | {"blemish_level": value}, None
                )
                self.assertEqual(result["status"], "incomplete_profile")
                self.assertTrue(result["message"])
                self.assertEqual(result["results"], [])

    def test_missing_blemish_level_returns_incomplete_profile(self):
        del self.profile["blemish_level"]
        result = self.module.recommend(self.profile, None)
        self.assertEqual(result["status"], "incomplete_profile")
        self.assertTrue(result["message"])
        self.assertEqual(result["results"], [])

    def test_numpy_integer_levels_follow_existing_routes(self):
        for dtype in (np.int32, np.int64):
            for level in range(1, 6):
                with self.subTest(dtype=dtype, level=level):
                    expected = "eligible" if level <= 3 else "referral"
                    self.assertEqual(self.module.check_scope(
                        self.profile | {"blemish_level": dtype(level)}), expected)

    def test_numpy_invalid_values_do_not_reach_ranking(self):
        for value in (np.bool_(True), np.float64(2), np.int64(0), np.int64(6)):
            with self.subTest(value=value):
                result = self.module.recommend(self.profile | {"blemish_level": value}, None)
                self.assertEqual(result["status"], "incomplete_profile")
                self.assertEqual(result["results"], [])

    def test_existing_early_exit_routes(self):
        for changes, expected in (
            ({"is_adult": False}, "referral"),
            ({"is_adult": None}, "incomplete_profile"),
            ({"concern": "other"}, "out_of_scope"),
            ({"blemish_level": 4}, "referral"),
            ({"blemish_level": 5}, "referral"),
            ({"referral_flags": ["prescribed_treatment"]}, "referral"),
        ):
            with self.subTest(changes=changes):
                result = self.module.recommend(self.profile | changes, None)
                self.assertEqual(result["status"], expected)
                self.assertTrue(result["message"])
                self.assertEqual(result["results"], [])


if __name__ == "__main__":
    unittest.main()
