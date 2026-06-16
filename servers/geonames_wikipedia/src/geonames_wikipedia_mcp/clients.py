from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

GEONAMES_BASE_URL = "https://secure.geonames.org"
MEDIAWIKI_API_URL = "https://en.wikipedia.org/w/api.php"
DEFAULT_TIMEOUT_SECONDS = 12


class ToolConfigurationError(RuntimeError):
    """Raised when required MCP tool configuration is missing."""


class RemoteServiceError(RuntimeError):
    """Raised when a remote service request fails."""


def geonames_username() -> str:
    username = os.getenv("GEONAMES_USERNAME", "").strip()
    if not username:
        raise ToolConfigurationError(
            "GEONAMES_USERNAME is required. Register and enable a GeoNames web-service account."
        )
    return username


def request_timeout_seconds() -> float:
    raw_value = os.getenv("GEONAMES_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)).strip()
    try:
        return max(1.0, float(raw_value))
    except ValueError:
        return float(DEFAULT_TIMEOUT_SECONDS)


def validate_latitude(latitude: float) -> float:
    value = float(latitude)
    if value < -90 or value > 90:
        raise ValueError("latitude must be between -90 and 90")
    return value


def validate_longitude(longitude: float) -> float:
    value = float(longitude)
    if value < -180 or value > 180:
        raise ValueError("longitude must be between -180 and 180")
    return value


def clamp_int(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


def clamp_float(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, float(value)))


def normalize_language(language: str | None) -> str:
    value = (language or "en").strip().lower()
    if not value or not value.replace("-", "").isalpha():
        return "en"
    return value[:12]


def build_url(base_url: str, path: str, params: dict[str, Any]) -> str:
    query = urlencode({key: value for key, value in params.items() if value is not None})
    if not path:
        return f"{base_url}?{query}"
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}?{query}"


def build_geonames_nearby_wikipedia_url(
    latitude: float,
    longitude: float,
    radius_km: float,
    max_rows: int,
    language: str,
    username: str,
) -> str:
    return build_url(
        GEONAMES_BASE_URL,
        "findNearbyWikipediaJSON",
        {
            "lat": validate_latitude(latitude),
            "lng": validate_longitude(longitude),
            "radius": clamp_float(radius_km, 0.1, 20.0),
            "maxRows": clamp_int(max_rows, 1, 50),
            "lang": normalize_language(language),
            "username": username,
        },
    )


def build_geonames_wikipedia_search_url(
    query: str,
    max_rows: int,
    language: str,
    username: str,
) -> str:
    return build_url(
        GEONAMES_BASE_URL,
        "wikipediaSearchJSON",
        {
            "q": query.strip(),
            "maxRows": clamp_int(max_rows, 1, 50),
            "lang": normalize_language(language),
            "username": username,
        },
    )


def build_mediawiki_opensearch_url(query: str, max_rows: int, language: str) -> str:
    language = normalize_language(language)
    parsed = urlparse(MEDIAWIKI_API_URL)
    host = f"{language}.wikipedia.org" if language != "en" else parsed.netloc
    base_url = f"{parsed.scheme}://{host}{parsed.path}"
    return build_url(
        base_url,
        "",
        {
            "action": "opensearch",
            "format": "json",
            "formatversion": 2,
            "namespace": 0,
            "limit": clamp_int(max_rows, 1, 20),
            "search": query.strip(),
        },
    )


def build_web_search_urls(query: str) -> dict[str, str]:
    encoded = urlencode({"q": query.strip()})
    return {
        "duckduckgo": f"https://duckduckgo.com/?{encoded}",
        "google": f"https://www.google.com/search?{encoded}",
        "bing": f"https://www.bing.com/search?{encoded}",
    }


def fetch_json(url: str, timeout_seconds: float | None = None) -> Any:
    request = Request(url, headers={"User-Agent": "geospatial-mcp-services/0.1"})
    try:
        with urlopen(request, timeout=timeout_seconds or request_timeout_seconds()) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RemoteServiceError(f"HTTP {exc.code} from {url}") from exc
    except URLError as exc:
        raise RemoteServiceError(f"Could not reach {url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RemoteServiceError(f"Invalid JSON returned by {url}") from exc


def normalize_geonames_article(entry: dict[str, Any]) -> dict[str, Any]:
    wikipedia_url = entry.get("wikipediaUrl") or ""
    if wikipedia_url and not wikipedia_url.startswith(("http://", "https://")):
        wikipedia_url = f"https://{wikipedia_url}"
    return {
        "title": entry.get("title") or "",
        "summary": entry.get("summary") or "",
        "feature": entry.get("feature") or "",
        "country_code": entry.get("countryCode") or "",
        "latitude": _optional_float(entry.get("lat")),
        "longitude": _optional_float(entry.get("lng")),
        "distance_km": _optional_float(entry.get("distance")),
        "elevation": _optional_float(entry.get("elevation")),
        "wikipedia_url": wikipedia_url,
        "thumbnail_url": entry.get("thumbnailImg") or "",
        "raw": entry,
    }


def normalize_mediawiki_opensearch(payload: list[Any]) -> dict[str, Any]:
    query = payload[0] if len(payload) > 0 else ""
    titles = payload[1] if len(payload) > 1 and isinstance(payload[1], list) else []
    descriptions = payload[2] if len(payload) > 2 and isinstance(payload[2], list) else []
    urls = payload[3] if len(payload) > 3 and isinstance(payload[3], list) else []
    results = []
    for index, title in enumerate(titles):
        results.append(
            {
                "title": title,
                "description": descriptions[index] if index < len(descriptions) else "",
                "url": urls[index] if index < len(urls) else "",
            }
        )
    return {"query": query, "results": results}


def selected_search_query(
    supplied_query: str | None,
    articles: list[dict[str, Any]],
    latitude: float,
    longitude: float,
) -> str:
    if supplied_query and supplied_query.strip():
        return supplied_query.strip()
    first_title = next((article["title"] for article in articles if article.get("title")), "")
    if first_title:
        return first_title
    return f"{latitude:.6f},{longitude:.6f} nearby geography"


def explore_point(
    latitude: float,
    longitude: float,
    radius_km: float = 10,
    max_rows: int = 10,
    language: str = "en",
    query: str | None = None,
    include_mediawiki_search: bool = True,
) -> dict[str, Any]:
    latitude = validate_latitude(latitude)
    longitude = validate_longitude(longitude)
    radius_km = clamp_float(radius_km, 0.1, 20.0)
    max_rows = clamp_int(max_rows, 1, 50)
    language = normalize_language(language)
    username = geonames_username()

    nearby_url = build_geonames_nearby_wikipedia_url(
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        max_rows=max_rows,
        language=language,
        username=username,
    )
    nearby_payload = fetch_json(nearby_url)
    status = nearby_payload.get("status") if isinstance(nearby_payload, dict) else None
    if status:
        raise RemoteServiceError(status.get("message") or "GeoNames returned an error status.")

    raw_articles = nearby_payload.get("geonames", []) if isinstance(nearby_payload, dict) else []
    articles = [normalize_geonames_article(entry) for entry in raw_articles if isinstance(entry, dict)]
    search_query = selected_search_query(query, articles, latitude, longitude)

    mediawiki = None
    mediawiki_url = None
    if include_mediawiki_search and search_query:
        mediawiki_url = build_mediawiki_opensearch_url(search_query, max_rows=min(max_rows, 20), language=language)
        mediawiki = normalize_mediawiki_opensearch(fetch_json(mediawiki_url))

    return {
        "selected_point": {
            "latitude": latitude,
            "longitude": longitude,
            "radius_km": radius_km,
        },
        "nearby_wikipedia": articles,
        "wikipedia_search": mediawiki,
        "web_search_urls": build_web_search_urls(search_query),
        "source_urls": {
            "geonames_nearby_wikipedia": nearby_url,
            "mediawiki_opensearch": mediawiki_url,
        },
    }


def _optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
