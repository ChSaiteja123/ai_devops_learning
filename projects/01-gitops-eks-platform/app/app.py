import os
from flask import Flask, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

app = Flask(__name__)
REQUESTS = Counter("http_requests_total", "HTTP requests served", ["path", "status"])


@app.get("/")
def home():
    REQUESTS.labels(path="/", status="200").inc()
    return jsonify(service="sample-api", version=os.getenv("APP_VERSION", "dev"))


@app.get("/simulate-error")
def simulate_error():
    REQUESTS.labels(path="/simulate-error", status="500").inc()
    return jsonify(error="controlled test failure"), 500


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/ready")
def ready():
    return jsonify(status="ready")


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
