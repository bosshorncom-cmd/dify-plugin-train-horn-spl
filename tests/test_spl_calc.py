"""Unit tests for the free-field train horn SPL calculator.

These tests import only the pure calculation module (standard library)
and do not require the Dify plugin SDK or a running Dify instance.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.spl_calc import SplCalculationError, format_prediction, predict_spl


class PredictSplTests(unittest.TestCase):
    def test_tenfold_distance_drops_twenty_decibels(self) -> None:
        result = predict_spl(
            reference_spl_db=115,
            reference_distance_m=1,
            target_distance_m=10,
        )
        self.assertAlmostEqual(result["predicted_spl_db"], 95.0, places=9)
        self.assertAlmostEqual(result["geometric_spreading_db"], 20.0, places=9)
        self.assertEqual(result["atmospheric_absorption_db"], 0.0)
        self.assertEqual(result["attenuation_db_per_km"], 0.0)

    def test_doubling_distance_drops_about_six_decibels(self) -> None:
        result = predict_spl(100, 1, 2)
        expected_spread = 20.0 * math.log10(2)
        self.assertAlmostEqual(result["geometric_spreading_db"], expected_spread, places=12)
        self.assertAlmostEqual(result["predicted_spl_db"], 100.0 - expected_spread, places=12)

    def test_linear_absorption_uses_path_difference_in_kilometres(self) -> None:
        # 115 dB at 1 m, predicted at 1001 m, with a user-supplied 5 dB/km term.
        result = predict_spl(
            reference_spl_db=115,
            reference_distance_m=1,
            target_distance_m=1001,
            attenuation_db_per_km=5,
        )
        expected_spread = 20.0 * math.log10(1001 / 1)
        expected_abs = 5.0 * (1001 - 1) / 1000.0
        self.assertAlmostEqual(result["geometric_spreading_db"], expected_spread, places=12)
        self.assertAlmostEqual(result["atmospheric_absorption_db"], expected_abs, places=12)
        self.assertAlmostEqual(
            result["predicted_spl_db"],
            115.0 - expected_spread - expected_abs,
            places=12,
        )

    def test_closer_target_increases_level(self) -> None:
        result = predict_spl(80, 10, 5)
        self.assertAlmostEqual(result["geometric_spreading_db"], 20.0 * math.log10(0.5), places=12)
        self.assertGreater(result["predicted_spl_db"], 80.0)

    def test_default_attenuation_is_zero(self) -> None:
        with_default = predict_spl(90, 2, 8)
        with_explicit = predict_spl(90, 2, 8, attenuation_db_per_km=0)
        self.assertEqual(with_default["predicted_spl_db"], with_explicit["predicted_spl_db"])
        self.assertEqual(with_default["atmospheric_absorption_db"], 0.0)

    def test_string_numbers_are_accepted(self) -> None:
        result = predict_spl("110", "1.0", "10", "0")
        self.assertAlmostEqual(result["predicted_spl_db"], 90.0, places=9)

    def test_zero_or_negative_distance_is_rejected(self) -> None:
        with self.assertRaises(SplCalculationError):
            predict_spl(100, 0, 10)
        with self.assertRaises(SplCalculationError):
            predict_spl(100, 1, -3)

    def test_non_numeric_and_non_finite_inputs_are_rejected(self) -> None:
        with self.assertRaises(SplCalculationError):
            predict_spl("loud", 1, 10)
        with self.assertRaises(SplCalculationError):
            predict_spl(100, 1, math.inf)
        with self.assertRaises(SplCalculationError):
            predict_spl(100, 1, 10, attenuation_db_per_km=math.nan)

    def test_summary_mentions_free_field_and_train_horn(self) -> None:
        text = format_prediction(predict_spl(115, 1, 10))
        self.assertIn("train horn", text)
        self.assertIn("Free-field", text)
        self.assertIn("95.00 dB", text)
        self.assertIn("ISO 9613", text)


if __name__ == "__main__":
    unittest.main()
