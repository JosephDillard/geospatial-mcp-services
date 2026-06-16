from __future__ import annotations

import unittest

from geonames_wikipedia_mcp.clients import (
    build_geonames_nearby_wikipedia_url,
    build_mediawiki_opensearch_url,
    build_web_search_urls,
    normalize_geonames_article,
    normalize_language,
    normalize_mediawiki_opensearch,
    selected_search_query,
    validate_latitude,
    validate_longitude,
)


class ClientHelperTests(unittest.TestCase):
    def test_validate_coordinates(self) -> None:
        self.assertEqual(validate_latitude(35.0), 35.0)
        self.assertEqual(validate_longitude(-106.5), -106.5)
        with self.assertRaises(ValueError):
            validate_latitude(91)
        with self.assertRaises(ValueError):
            validate_longitude(-181)

    def test_build_geonames_nearby_url(self) -> None:
        url = build_geonames_nearby_wikipedia_url(
            latitude=35.0402,
            longitude=-106.5317,
            radius_km=10,
            max_rows=8,
            language="en",
            username="example",
        )
        self.assertIn("findNearbyWikipediaJSON", url)
        self.assertIn("lat=35.0402", url)
        self.assertIn("lng=-106.5317", url)
        self.assertIn("username=example", url)

    def test_build_mediawiki_url_uses_language_host(self) -> None:
        url = build_mediawiki_opensearch_url("Kirtland AFB", 5, "es")
        self.assertTrue(url.startswith("https://es.wikipedia.org/w/api.php?"))
        self.assertIn("action=opensearch", url)
        self.assertIn("search=Kirtland+AFB", url)

    def test_normalizers(self) -> None:
        self.assertEqual(normalize_language("EN"), "en")
        self.assertEqual(normalize_language("bad value!"), "en")
        article = normalize_geonames_article(
            {
                "title": "Example",
                "lat": "35.1",
                "lng": "-106.6",
                "distance": "1.25",
                "wikipediaUrl": "en.wikipedia.org/wiki/Example",
            }
        )
        self.assertEqual(article["latitude"], 35.1)
        self.assertEqual(article["distance_km"], 1.25)
        self.assertEqual(article["wikipedia_url"], "https://en.wikipedia.org/wiki/Example")

    def test_mediawiki_opensearch_normalizer(self) -> None:
        payload = ["query", ["Title"], ["Description"], ["https://example.test"]]
        normalized = normalize_mediawiki_opensearch(payload)
        self.assertEqual(normalized["query"], "query")
        self.assertEqual(normalized["results"][0]["title"], "Title")

    def test_selected_search_query(self) -> None:
        self.assertEqual(
            selected_search_query("supplied", [{"title": "Nearby"}], 35, -106),
            "supplied",
        )
        self.assertEqual(
            selected_search_query(None, [{"title": "Nearby"}], 35, -106),
            "Nearby",
        )
        self.assertIn("35.000000,-106.000000", selected_search_query(None, [], 35, -106))

    def test_web_search_urls(self) -> None:
        urls = build_web_search_urls("Kirtland AFB")
        self.assertIn("duckduckgo", urls)
        self.assertIn("Kirtland+AFB", urls["google"])


if __name__ == "__main__":
    unittest.main()
