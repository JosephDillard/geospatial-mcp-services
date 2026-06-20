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
        self.assertEqual(validate_latitude(35.9), 35.9)
        self.assertEqual(validate_longitude(-105.9), -105.9)
        with self.assertRaises(ValueError):
            validate_latitude(91)
        with self.assertRaises(ValueError):
            validate_longitude(-181)

    def test_validate_radius(self) -> None:
        self.assertEqual(validate_radius(5), 5)
        with self.assertRaises(ValueError):
            validate_radius(0)
        with self.assertRaises(ValueError):
            validate_radius(251)

    def test_distance_is_reasonable(self) -> None:
        self.assertLess(distance_km(35.6870, -105.9378, 35.6932, -105.9446), 1)

    def test_analyze_point_returns_nearby_context(self) -> None:
        result = analyze_point(latitude=35.6870, longitude=-105.9378, radius_km=220)

        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(result["incident_count"], 1)
        self.assertGreaterEqual(result["asset_count"], 1)
        self.assertIn(result["risk"]["level"], {"low", "medium", "high"})
        self.assertTrue(result["recommended_actions"])
        categories = {item["category"] for item in result["nearby_incidents"]}
        self.assertIn("disaster_relief", categories)
        self.assertIn("force_protection", categories)

    def test_analyze_point_without_nearby_context(self) -> None:
        result = analyze_point(latitude=34.0, longitude=-103.0, radius_km=10)

        self.assertEqual(result["incident_count"], 0)
        self.assertEqual(result["asset_count"], 0)
        self.assertEqual(result["risk"]["level"], "none")


if __name__ == "__main__":
    unittest.main()
