# Incident Analyst MCP

Incident Analyst MCP is a Docker-ready Model Context Protocol server for map-click
incident analysis. It accepts a selected latitude/longitude, finds nearby synthetic
operational incidents and critical assets, scores risk, and returns a concise
operator-facing summary.

This server is intentionally deterministic and offline-friendly. It is designed to
prove the tool contract before connecting to a live PostGIS layer, status-board
API, or enterprise incident feed.

## Tool

```text
analyze_incident_point
```

Example arguments:

```json
{
  "latitude": 32.9312,
  "longitude": -96.4597,
  "radius_km": 5,
  "max_incidents": 5,
  "include_assets": true
}
```

## Local Test

```powershell
$env:PYTHONPATH = "servers/incident_analyst/src"
python -m unittest discover -s servers/incident_analyst/tests -v
Remove-Item Env:PYTHONPATH
```

## Docker

```powershell
docker build `
  -t geospatial-mcp/incident-analyst:local `
  -f servers/incident_analyst/Dockerfile `
  servers/incident_analyst
```

Run as an MCP stdio server:

```powershell
docker run --rm -i geospatial-mcp/incident-analyst:local
```
