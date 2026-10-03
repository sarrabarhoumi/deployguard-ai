from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze():
    payload = {
        "repository": "deployguard-demo",
        "branch": "feature/payment",
        "commit_sha": "a83f12",
        "diff": "example diff"
    }

    response = client.post(
        "/api/v1/analyze",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "risk_score" in data
    assert "risk_level" in data