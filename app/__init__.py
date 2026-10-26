import os
import socket
import time

from flask import Flask, g, jsonify, render_template, request
from prometheus_client import Counter, Gauge, Histogram, start_http_server

from .catalog import CATALOG, CATEGORY_ORDER, PRESETS
from .compat import evaluate

APP_VERSION = os.getenv("APP_VERSION", "dev")
APP_ENV = os.getenv("APP_ENV", "local")
POD_NAME = os.getenv("POD_NAME", socket.gethostname())

REQUESTS = Counter("pcforge_http_requests_total", "HTTP requests", ["method", "endpoint", "status"])
LATENCY = Histogram("pcforge_http_request_duration_seconds", "Request latency", ["endpoint"],
                    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5))
BUILD_CHECKS = Counter("pcforge_build_checks_total", "Build compatibility checks", ["result"])
INFO = Gauge("pcforge_build_info", "App version info", ["version", "env"])
INFO.labels(APP_VERSION, APP_ENV).set(1)


def create_app():
    app = Flask(__name__)

    @app.before_request
    def _start_timer():
        g.start = time.perf_counter()

    @app.after_request
    def _record(response):
        endpoint = request.url_rule.rule if request.url_rule else "unmatched"
        LATENCY.labels(endpoint).observe(time.perf_counter() - g.start)
        REQUESTS.labels(request.method, endpoint, response.status_code).inc()
        return response

    @app.get("/")
    def index():
        return render_template("index.html", version=APP_VERSION, env=APP_ENV, pod=POD_NAME)

    @app.get("/api/parts")
    def parts():
        return jsonify({"order": CATEGORY_ORDER, "catalog": CATALOG,
                        "presets": {k: {"label": v["label"], "parts": v["parts"]} for k, v in PRESETS.items()}})

    @app.post("/api/check")
    def check():
        body = request.get_json(silent=True) or {}
        selection = body.get("parts")
        if not isinstance(selection, dict):
            return jsonify({"error": "expected JSON body {\"parts\": {category: id}}"}), 400
        result = evaluate(selection)
        BUILD_CHECKS.labels(result["status"]).inc()
        return jsonify(result)

    @app.get("/version")
    def version():
        return jsonify({"version": APP_VERSION, "env": APP_ENV, "pod": POD_NAME})

    # Liveness: the process is up. Keep it dumb so a slow dependency never gets the pod killed.
    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "alive"})

    # Readiness: safe to receive traffic. The catalog is in-process, so ready once it is loaded.
    @app.get("/readyz")
    def readyz():
        ready = all(CATALOG.get(c) for c in CATEGORY_ORDER)
        return jsonify({"status": "ready" if ready else "not-ready"}), (200 if ready else 503)

    return app


_metrics_server_started = False


def start_metrics_server():
    """Serve Prometheus metrics on their own port (METRICS_PORT), never on the app port.
    The Ingress only routes to the app port, so /metrics is not reachable from the internet."""
    global _metrics_server_started
    port = os.getenv("METRICS_PORT")
    if port and not _metrics_server_started:
        start_http_server(int(port))
        _metrics_server_started = True


app = create_app()
start_metrics_server()
