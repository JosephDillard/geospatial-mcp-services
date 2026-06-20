from __future__ import annotations

import unittest

from incident_analyst_mcp.analysis import (
    analyze_point,
    distance_km,
    validate_latitude,
    validate_longitude,
    validate_radius,
)


class IncidentAnalysisTests(unittest.TestCase):
    def test_validate_coordinates(self) -> None:
        self.assertEqual(validate_latitude(32.9), 32.9)
        self.assertEqual(validate_longitude(-96.4), -96.4)
        with self.assertRaises(ValueError):
            validate_latitude(91)
        with self.assertRaises(ValueError):
            validate_longitude(-181)

    def test_validate_radius(self) -> None:
        self.assertEqual(validate_radius(5), 5)
        with self.assertRaises(ValueError):
            validate_radius(0)
        with self.assertRaises(ValueError):
            validate_radius(101)

    def test_distance_is_reasonable(self) -> None:
        self.assertLess(distance_km(32.9312, -96.4597, 32.9324, -96.4605), 1)

    def test_analyze_point_returns_nearby_context(self) -> None:
        result = analyze_point(latitude=32.9312, longitude=-96.4597, radius_km=5)

        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(result["incident_count"], 1)
        self.assertGreaterEqual(result["asset_count"], 1)
        self.assertIn(result["risk"]["level"], {"low", "medium", "high"})
        self.assertTrue(result["recommended_actions"])

    def test_analyze_point_without_nearby_context(self) -> None:
        result = analyze_point(latitude=33.5, longitude=-97.2, radius_km=1)

        self.assertEqual(result["incident_count"], 0)
        self.assertEqual(result["asset_count"], 0)
        self.assertEqual(result["risk"]["level"], "none")


if __name__ == "__main__":
    unittest.main()
