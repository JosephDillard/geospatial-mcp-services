[Portfolio Home: Joseph C. Dillard Geospatial Project Stack](https://josephdillard.github.io/JosephDillard/)

# Incident Analyst MCP

Incident Analyst MCP is a Docker-ready Model Context Protocol server for map-click
incident analysis. It accepts a selected latitude/longitude, finds nearby synthetic
operational incidents and critical assets, scores risk, and returns a concise
operator-facing summary.

This server is intentionally deterministic and offline-friendly. It is designed to
prove the tool contract before connecting to a live PostGIS layer, status-board
API, or enterprise incident feed.

The sample data covers northern New Mexico from Santa Fe toward the Colorado
border, including utility, weather, communications, disaster-relief, and
force-protection incidents.

## Fit With The Stack

This server owns the deterministic MCP incident-analysis tool. The
local `map-to-ai-incident-analyst` repo provides a standalone browser bridge/demo, and
the `geospatial-status-board` Incident Analyst route can call that bridge through
same-origin app proxy routes while keeping MCP transport out of the browser.

Related repos:

- Map-to-AI Incident Analyst bridge/demo (local repo; GitHub publication pending)
- [Geospatial Status Board](https://github.com/JosephDillard/geospatial-status-board)
- [Root MCP services README](../../README.md)

## Tool

```text
analyze_incident_point
```

Example arguments:

```json
{
  "latitude": 35.6870,
  "longitude": -105.9378,
  "radius_km": 220,
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
