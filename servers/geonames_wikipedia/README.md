# GeoNames Wikipedia MCP

MCP server for enriching a selected map point with GeoNames and Wikipedia context.

## Tool

```text
explore_point_with_geonames
```

The tool accepts `latitude` and `longitude`, then searches GeoNames nearby Wikipedia
entries. It also runs a Wikipedia OpenSearch query using either the supplied `query`
or the best nearby article title.

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
