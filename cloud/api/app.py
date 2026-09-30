"""Lightweight, framework-neutral WSGI application for AeroTrust AI Verification API."""
from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from cloud.api.health import get_health
from cloud.api.maintenance import (
    close_maintenance,
    get_maintenance_state,
    mark_maintenance_started,
    perform_retest,
)
from cloud.api.passport import get_passport
from cloud.api.verification import ingest_and_verify, verification_status
from cloud.storage.store import get_default_store


def wsgi_app(environ: dict[str, Any], start_response: Callable) -> list[bytes]:
    """WSGI application handling AeroTrust verification and maintenance endpoints."""
    path: str = environ.get("PATH_INFO", "/").rstrip("/") or "/"
    method: str = environ.get("REQUEST_METHOD", "GET").upper()

    def respond(status: str, data: Any) -> list[bytes]:
        body = json.dumps(data).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
            ("Access-Control-Allow-Headers", "Content-Type"),
        ]
        start_response(status, headers)
        return [body]

    if method == "OPTIONS":
        return respond("200 OK", {"status": "ok"})

    # Read body for POST
    post_data: dict[str, Any] = {}
    if method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0) or 0)
            if content_length > 0:
                raw_body = environ["wsgi.input"].read(content_length)
                post_data = json.loads(raw_body.decode("utf-8"))
        except (json.JSONDecodeError, ValueError) as e:
            return respond("400 Bad Request", {"error": f"Invalid JSON body: {e!s}"})

    store = get_default_store()

    # Route: GET /health
    if path == "/health" and method == "GET":
        return respond("200 OK", get_health())

    # Route: POST /verification/events
    if path == "/verification/events" and method == "POST":
        outcome = ingest_and_verify(post_data, store=store)
        status_code = "200 OK" if outcome.get("verified") else "400 Bad Request"
        return respond(status_code, outcome)

    # Route: GET /verification/{report_id}
    if path.startswith("/verification/") and method == "GET":
        report_id = path.split("/verification/", 1)[1]
        res = verification_status(report_id, store=store)
        status_code = "200 OK" if res.get("status") != "NOT_FOUND" else "404 Not Found"
        return respond(status_code, res)

    # Route: GET /maintenance/{asset_id}
    if path.startswith("/maintenance/") and method == "GET":
        asset_id = path.split("/maintenance/", 1)[1]
        return respond("200 OK", get_maintenance_state(asset_id, store=store))

    # Route: POST /maintenance/{report_id}/start
    if path.startswith("/maintenance/") and path.endswith("/start") and method == "POST":
        report_id = path.split("/maintenance/")[1].split("/start")[0]
        try:
            res = mark_maintenance_started(report_id, store=store)
            return respond("200 OK", res)
        except KeyError as e:
            return respond("404 Not Found", {"error": str(e)})

    # Route: POST /maintenance/retest
    if path == "/maintenance/retest" and method == "POST":
        try:
            res = perform_retest(
                report_id=post_data["report_id"],
                fresh_features=post_data["fresh_features"],
                store=store,
            )
            return respond("200 OK", res)
        except KeyError as e:
            return respond("400 Bad Request", {"error": str(e)})

    # Route: POST /maintenance/closure
    if path == "/maintenance/closure" and method == "POST":
        try:
            res = close_maintenance(
                report_id=post_data["report_id"],
                maintenance_action=post_data["maintenance_action"],
                post_health_score=float(post_data["post_health_score"]),
                store=store,
            )
            return respond("200 OK", res)
        except KeyError as e:
            return respond("400 Bad Request", {"error": str(e)})

    # Route: GET /passport/{component_id}
    if path.startswith("/passport/") and method == "GET":
        component_id = path.split("/passport/", 1)[1]
        return respond("200 OK", get_passport(component_id, store=store))

    return respond("404 Not Found", {"error": f"Endpoint not found: {method} {path}"})


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    port = 8000
    print(f"AeroTrust AI Verification API running on port {port}...")
    server = make_server("127.0.0.1", port, wsgi_app)
    server.serve_forever()
