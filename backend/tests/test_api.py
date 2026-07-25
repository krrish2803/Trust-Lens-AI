"""
TrustLens AI - FastAPI Endpoint Integration Tests
"""

import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data["components"]


def test_scan_url_endpoint():
    payload = {"url": "http://sbi-kyc-update.online"}
    response = client.post("/scan/url", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert data["scan_type"] == "url"
    assert data["verdict"] in ["Safe", "Low Risk", "Medium Risk", "High Risk", "Critical"]


def test_scan_message_endpoint():
    payload = {"text": "Aapka account block ho jayega! OTP share karo turant.", "channel": "sms"}
    response = client.post("/scan/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] > 50
    assert data["scam_category"] != ""


def test_get_history_endpoint():
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
