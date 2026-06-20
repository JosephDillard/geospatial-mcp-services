from __future__ import annotations


SAMPLE_INCIDENTS = [
    {
        "incident_id": "INC-1001",
        "title": "Substation transformer alarm",
        "category": "utility",
        "severity": "high",
        "status": "active",
        "latitude": 32.9324,
        "longitude": -96.4605,
        "summary": "Telemetry indicates heat and load anomalies at a distribution transformer.",
    },
    {
        "incident_id": "INC-1002",
        "title": "Feeder line vegetation contact",
        "category": "utility",
        "severity": "medium",
        "status": "monitoring",
        "latitude": 32.9391,
        "longitude": -96.4554,
        "summary": "Field crew reported vegetation contact near a feeder corridor.",
    },
    {
        "incident_id": "INC-1003",
        "title": "Road closure near service corridor",
        "category": "transportation",
        "severity": "medium",
        "status": "active",
        "latitude": 32.9272,
        "longitude": -96.4688,
        "summary": "Lane closure may affect crew routing and incident response time.",
    },
    {
        "incident_id": "INC-1004",
        "title": "Public safety event downtown",
        "category": "public_safety",
        "severity": "low",
        "status": "monitoring",
        "latitude": 32.9259,
        "longitude": -96.4478,
        "summary": "Local event increases traffic and pedestrian activity near downtown assets.",
    },
]


SAMPLE_ASSETS = [
    {
        "asset_id": "AST-2001",
        "name": "North Rockwall Substation",
        "asset_type": "substation",
        "criticality": "high",
        "latitude": 32.9317,
        "longitude": -96.4591,
    },
    {
        "asset_id": "AST-2002",
        "name": "Feeder 12 switching cabinet",
        "asset_type": "switch",
        "criticality": "medium",
        "latitude": 32.9371,
        "longitude": -96.4561,
    },
    {
        "asset_id": "AST-2003",
        "name": "Downtown crew staging yard",
        "asset_type": "operations",
        "criticality": "medium",
        "latitude": 32.9261,
        "longitude": -96.4499,
    },
]
