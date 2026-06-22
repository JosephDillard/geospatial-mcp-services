[Portfolio Home: Joseph C. Dillard Geospatial Project Stack](https://josephdillard.github.io/JosephDillard/)

# GeoNames Wikipedia MCP

MCP server for enriching a selected map point with GeoNames and Wikipedia context.

## Tool

```text
explore_point_with_geonames
```

The tool accepts `latitude` and `longitude`, then searches GeoNames nearby Wikipedia
entries. It also runs a Wikipedia OpenSearch query using either the supplied `query`
or the best nearby article title.

## Fit With The Stack

This server backs the map-click place-context story for the broader portfolio.
The `geospatial-status-board` map currently exposes Wiki/GeoNames exploration as
a browser map tool; future MCP-aware hosts or bridge services can call this MCP
server using the same point-input contract.

Related docs:

- [Root MCP services README](../../README.md)
- [Map point tool contract](../../docs/map-point-tool-contract.md)
- [Geospatial Status Board](https://github.com/JosephDillard/geospatial-status-board)

## Environment

```text
GEONAMES_USERNAME=your_geonames_username
GEONAMES_TIMEOUT_SECONDS=12
```

## Run

```powershell
python -m geonames_wikipedia_mcp.server
```

Docker:

```powershell
docker run --rm -i `
  -e GEONAMES_USERNAME=$env:GEONAMES_USERNAME `
  geospatial-mcp/geonames-wikipedia:local
```
