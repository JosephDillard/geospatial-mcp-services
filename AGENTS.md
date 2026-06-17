# Agent Guide

This repo contains Docker-ready Model Context Protocol servers for geospatial
assistant workflows. Each MCP server should stand on its own while sharing root
documentation and Docker/config examples.

## Stack Context

Related sibling repos:

- `geospatial-status-board` is the map viewer that can eventually call MCP tools
  from map clicks or selected features.
- `geospatial-data-gateway` loads and refreshes PostGIS layers that can provide
  context for assistant tools.
- `geoai-asset-detection-platform` creates GeoAI outputs that may become map
  layers or assistant context.

When changing cross-repo docs, prefer full GitHub URLs for links that point
outside this repo.

## What This Repo Owns

- MCP servers: `servers/<server_name>/`
- First server: `servers/geonames_wikipedia/`
- GeoNames/Wikipedia package:
  `servers/geonames_wikipedia/src/geonames_wikipedia_mcp/`
- MCP host config examples: `configs/`
- Map-click contract docs: `docs/map-point-tool-contract.md`
- Local image helpers: `docker-compose.yml`

The first tool is `explore_point_with_geonames`, which accepts latitude and
longitude from a map click and returns nearby GeoNames/Wikipedia context plus
transparent source/search URLs.

## Development Notes

- MCP servers should use stdio transport by default so Docker-based MCP hosts can
  launch them predictably.
- Keep server-specific code, tests, Dockerfiles, and package metadata under that
  server's folder.
- Keep GeoNames credentials in `GEONAMES_USERNAME` or `.env`; never commit real
  usernames, API keys, tokens, or host-specific secrets.
- Unit tests should avoid live network calls. Mock or isolate GeoNames and
  MediaWiki client behavior.
- General web search is currently represented as generated search URLs rather
  than a paid search API call.
- Use EPSG:4326 latitude/longitude for map-click tool inputs unless the contract
  explicitly changes.

## Useful Commands

GeoNames/Wikipedia server tests:

```powershell
$env:PYTHONPATH = "servers/geonames_wikipedia/src"
python -m unittest discover -s servers/geonames_wikipedia/tests -v
Remove-Item Env:PYTHONPATH
```

Build the first MCP image:

```powershell
docker build `
  -t geospatial-mcp/geonames-wikipedia:local `
  -f servers/geonames_wikipedia/Dockerfile `
  servers/geonames_wikipedia
```

Run as a Docker stdio MCP server:

```powershell
docker run --rm -i `
  -e GEONAMES_USERNAME=$env:GEONAMES_USERNAME `
  geospatial-mcp/geonames-wikipedia:local
```

## Before Finishing Changes

- Run the relevant server unit tests.
- Build the touched server image when Dockerfiles, dependencies, or entrypoints
  change.
- Update `configs/mcp.docker.example.json`, `README.md`, and
  `docs/map-point-tool-contract.md` when tool names, arguments, return payloads,
  or Docker commands change.
