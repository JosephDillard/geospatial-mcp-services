from __future__ import annotations

import math
from typing import Any
from urllib.parse import quote_plus

from incident_analyst_mcp.sample_data import SAMPLE_ASSETS, SAMPLE_INCIDENTS


SEVERITY_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

CRITICALITY_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def analyze_point(
    *,
    latitude: float,
    longitude: float,
    radius_km: float = 5,
    max_incidents: int = 5,
    include_assets: bool = True,
) -> dict[str, Any]:
    lat = validate_latitude(latitude)
    lon = validate_longitude(longitude)
    radius = validate_radius(radius_km)
    max_rows = max(1, min(int(max_incidents), 20))

    nearby_incidents = sorted(
        [
            enrich_with_distance(incident, lat, lon)
            for incident in SAMPLE_INCIDENTS
            if distance_km(lat, lon, incident["latitude"], incident["longitude"]) <= radius
        ],
        key=lambda item: item["distance_km"],
    )[:max_rows]

    nearby_assets = []
    if include_assets:
        nearby_assets = sorted(
            [
                enrich_with_distance(asset, lat, lon)
                for asset in SAMPLE_ASSETS
                if distance_km(lat, lon, asset["latitude"], asset["longitude"]) <= radius
            ],
            key=lambda item: item["distance_km"],
        )

    risk = score_operational_risk(nearby_incidents, nearby_assets)
    return {
        "status": "ok",
        "selected_point": {
            "latitude": lat,
            "longitude": lon,
            "radius_km": radius,
        },
        "incident_count": len(nearby_incidents),
        "asset_count": len(nearby_assets),
        "nearby_incidents": nearby_incidents,
        "nearby_assets": nearby_assets,
        "risk": risk,
        "operator_summary": build_operator_summary(nearby_incidents, nearby_assets, risk),
        "recommended_actions": recommended_actions(nearby_incidents, nearby_assets, risk),
        "web_search_urls": build_search_urls(lat, lon, nearby_incidents),
    }


def validate_latitude(value: float) -> float:
    lat = float(value)
    if not -90 <= lat <= 90:
        raise ValueError("Latitude must be between -90 and 90.")
    return lat


def validate_longitude(value: float) -> float:
    lon = float(value)
    if not -180 <= lon <= 180:
        raise ValueError("Longitude must be between -180 and 180.")
    return lon


def validate_radius(value: float) -> float:
    radius = float(value)
    if radius <= 0 or radius > 100:
        raise ValueError("Radius must be greater than 0 and no more than 100 km.")
    return radius


def enrich_with_distance(item: dict[str, Any], latitude: float, longitude: float) -> dict[str, Any]:
    enriched = dict(item)
    enriched["distance_km"] = round(
        distance_km(latitude, longitude, item["latitude"], item["longitude"]),
        3,
    )
    return enriched


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def score_operational_risk(
    incidents: list[dict[str, Any]],
    assets: list[dict[str, Any]],
) -> dict[str, Any]:
    incident_score = sum(SEVERITY_SCORE.get(str(item.get("severity", "low")), 1) for item in incidents)
    asset_score = sum(CRITICALITY_SCORE.get(str(item.get("criticality", "low")), 1) for item in assets)
    proximity_bonus = 2 if incidents and incidents[0]["distance_km"] <= 1 else 0
    total = incident_score + asset_score + proximity_bonus

    if total >= 10:
        level = "high"
    elif total >= 5:
        level = "medium"
    elif total > 0:
        level = "low"
    else:
        level = "none"

    return {
        "level": level,
        "score": total,
        "incident_score": incident_score,
        "asset_score": asset_score,
        "proximity_bonus": proximity_bonus,
    }


def build_operator_summary(
    incidents: list[dict[str, Any]],
    assets: list[dict[str, Any]],
    risk: dict[str, Any],
) -> str:
    if not incidents and not assets:
        return "No nearby incidents or critical assets were found inside the selected radius."

    incident_text = f"{len(incidents)} nearby incident(s)"
    asset_text = f"{len(assets)} nearby asset(s)"
    return (
        f"{incident_text} and {asset_text} were found. "
        f"Operational risk is {risk['level']} with score {risk['score']}."
    )


def recommended_actions(
    incidents: list[dict[str, Any]],
    assets: list[dict[str, Any]],
    risk: dict[str, Any],
) -> list[str]:
    actions = []
    if risk["level"] in {"high", "medium"}:
        actions.append("Review active incidents and confirm ownership before dispatch.")
    if any(item.get("severity") in {"high", "critical"} for item in incidents):
        actions.append("Prioritize high-severity incident verification and escalation.")
    if any(item.get("criticality") in {"high", "critical"} for item in assets):
        actions.append("Check impact to high-criticality assets inside the selected radius.")
    if not actions:
        actions.append("Monitor the area and refresh analysis if new incidents arrive.")
    return actions


def build_search_urls(
    latitude: float,
    longitude: float,
    incidents: list[dict[str, Any]],
) -> dict[str, str]:
    if incidents:
        query = f"{incidents[0]['title']} {latitude:.5f},{longitude:.5f}"
    else:
        query = f"incident context {latitude:.5f},{longitude:.5f}"
    encoded = quote_plus(query)
    return {
        "duckduckgo": f"https://duckduckgo.com/?q={encoded}",
        "google": f"https://www.google.com/search?q={encoded}",
        "bing": f"https://www.bing.com/search?q={encoded}",
    }
