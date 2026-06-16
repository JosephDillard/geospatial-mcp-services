from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from geonames_wikipedia_mcp.clients import (
    RemoteServiceError,
    ToolConfigurationError,
    explore_point,
)

mcp = FastMCP(
    "GeoNames Wikipedia",
    instructions=(
        "Use this server when a user selects a map point and wants nearby "
        "GeoNames/Wikipedia context or web-search links for that location."
    ),
)


@mcp.tool()
def explore_point_with_geonames(
    latitude: float,
    longitude: float,
    radius_km: float = 10,
    max_rows: int = 10,
    language: str = "en",
    query: str | None = None,
    include_mediawiki_search: bool = True,
) -> dict[str, Any]:
    """Enrich a selected map point with nearby GeoNames Wikipedia context.

    Use latitude/longitude from a map click. GeoNames provides nearby geotagged
    Wikipedia articles; MediaWiki OpenSearch optionally adds title-search results.
    """

    try:
        return explore_point(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            max_rows=max_rows,
            language=language,
            query=query,
            include_mediawiki_search=include_mediawiki_search,
        )
    except ToolConfigurationError as exc:
        return {
            "status": "configuration_required",
            "message": str(exc),
            "required_environment": ["GEONAMES_USERNAME"],
        }
    except (RemoteServiceError, ValueError) as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
