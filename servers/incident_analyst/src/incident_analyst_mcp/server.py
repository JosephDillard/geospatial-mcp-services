from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from incident_analyst_mcp.analysis import analyze_point

mcp = FastMCP(
    "Incident Analyst",
    instructions=(
        "Use this server when a user selects a map point and wants nearby "
        "incident, asset, operational-risk, and recommended-action context."
    ),
)


@mcp.tool()
def analyze_incident_point(
    latitude: float,
    longitude: float,
    radius_km: float = 120,
    max_incidents: int = 5,
    include_assets: bool = True,
) -> dict[str, Any]:
    """Analyze a selected map point against nearby synthetic incidents and assets."""

    try:
        return analyze_point(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            max_incidents=max_incidents,
            include_assets=include_assets,
        )
    except ValueError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
