# Geospatial MCP Services

Geospatial MCP Services is a home for Dockerized Model Context Protocol servers
that support geospatial workflows. The repo is structured so each MCP server can
stand alone, while shared Docker/config examples live at the root.

The first server is **GeoNames Wikipedia MCP**. It accepts a map-click coordinate,
uses GeoNames nearby Wikipedia data, and returns nearby articles plus Wikipedia and
web-search links.

## Repository Layout

```text
servers/
  geonames_wikipedia/       First MCP server: point -> GeoNames/Wikipedia context
configs/
  mcp.docker.example.json   MCP host config using Docker stdio
docs/
  map-point-tool-contract.md
docker-compose.yml          Local image build/run helper
```

## First MCP Tool

Tool name:

```text
explore_point_with_geonames
```

Example arguments from a map click:

```json
{
  "latitude": 35.0402,
  "longitude": -106.5317,
  "radius_km": 10,
  "max_rows": 8,
  "language": "en"
}
```

The tool returns:

- Nearby geotagged Wikipedia articles from GeoNames.
- A MediaWiki OpenSearch result set for the best nearby title or supplied query.
- Ready-to-open web search URLs for the selected point/context.
- The source URLs used for transparency and debugging.

## Requirements

GeoNames requires a registered username for web-service calls. Create and enable one
at:

```text
https://www.geonames.org/login
```

Then copy `.env.example` to `.env` and set:

```text
GEONAMES_USERNAME=your_geonames_username
```

## Build

```powershell
docker build `
  -t geospatial-mcp/geonames-wikipedia:local `
  -f servers/geonames_wikipedia/Dockerfile `
  servers/geonames_wikipedia
```

## Run As An MCP Server

MCP hosts normally launch stdio servers directly. The Docker command is:

```powershell
docker run --rm -i `
  -e GEONAMES_USERNAME=$env:GEONAMES_USERNAME `
  geospatial-mcp/geonames-wikipedia:local
```

Use [configs/mcp.docker.example.json](configs/mcp.docker.example.json) as the MCP
host config template.

## Local Dev Test

The unit tests avoid live network calls:

```powershell
$env:PYTHONPATH = "servers/geonames_wikipedia/src"
python -m unittest discover -s servers/geonames_wikipedia/tests -v
```

## Notes

- The Docker image uses MCP stdio transport by default.
- Additional MCP servers can be added under `servers/<name>/`.
- General web search is represented as generated search URLs so the server does not
  need a paid search API key.
