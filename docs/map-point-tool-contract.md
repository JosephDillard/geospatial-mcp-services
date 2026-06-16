# Map Point Tool Contract

The first MCP server is designed around a map-click workflow.

## Input

When the map viewer has a selected point, pass latitude and longitude to the MCP
tool:

```json
{
  "latitude": 35.0402,
  "longitude": -106.5317,
  "radius_km": 10,
  "max_rows": 8,
  "language": "en",
  "query": "optional place or incident context"
}
```

## Tool

```text
explore_point_with_geonames
```

## Output Shape

```json
{
  "selected_point": {
    "latitude": 35.0402,
    "longitude": -106.5317
  },
  "nearby_wikipedia": [
    {
      "title": "Kirtland Air Force Base",
      "summary": "...",
      "latitude": 35.05,
      "longitude": -106.56,
      "distance_km": 2.4,
      "wikipedia_url": "https://en.wikipedia.org/wiki/..."
    }
  ],
  "wikipedia_search": {
    "query": "Kirtland Air Force Base",
    "results": [
      {
        "title": "Kirtland Air Force Base",
        "description": "...",
        "url": "https://en.wikipedia.org/wiki/Kirtland_Air_Force_Base"
      }
    ]
  },
  "web_search_urls": {
    "duckduckgo": "https://duckduckgo.com/?q=...",
    "google": "https://www.google.com/search?q=...",
    "bing": "https://www.bing.com/search?q=..."
  }
}
```

## Map Integration Later

The status-board map can send the current click coordinate to an MCP-aware host or
server-side bridge. The bridge should call `explore_point_with_geonames` and render
returned links/context beside the map.
