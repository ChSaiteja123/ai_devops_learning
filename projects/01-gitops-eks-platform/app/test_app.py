from app import app


def test_health_and_readiness():
    client = app.test_client()
    assert client.get("/health").json == {"status": "ok"}
    assert client.get("/ready").json == {"status": "ready"}


def test_home_has_version():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.json["service"] == "sample-api"
    assert "version" in response.json


def test_controlled_error_increments_error_metric():
    client = app.test_client()
    response = client.get("/simulate-error")
    assert response.status_code == 500
    assert response.json == {"error": "controlled test failure"}
    metrics = client.get("/metrics").data
    assert b'http_requests_total{path="/simulate-error",status="500"}' in metrics
