from app import create_app
from app.catalog import CATALOG, PRESETS
from app.compat import evaluate


def client():
    return create_app().test_client()


def levels(result, category):
    return [i["level"] for i in result["issues"] if i["category"] == category]


def test_good_presets_are_compatible():
    for key in ("1440p-gaming", "small-form-factor", "workstation"):
        result = evaluate(PRESETS[key]["parts"])
        assert result["status"] == "ok", (key, result["issues"])


def test_broken_preset_catches_every_problem():
    result = evaluate(PRESETS["broken"]["parts"])
    assert result["status"] == "incompatible"
    for category in ("motherboard", "memory", "case", "gpu", "psu"):
        assert "error" in levels(result, category), category


def test_socket_mismatch():
    result = evaluate({"cpu": "i5-14600k", "motherboard": "b650-tomahawk"})
    assert "error" in levels(result, "motherboard")


def test_ddr4_board_with_intel_cpu_is_fine():
    result = evaluate({"cpu": "i5-14600k", "motherboard": "b760m-ds3h", "memory": "ddr4-32-3200"})
    assert result["issues"] == []


def test_air_cooler_too_tall_for_case():
    result = evaluate({"cooler": "nhd15g2", "case": "nr200p"})
    assert "error" in levels(result, "cooler")


def test_psu_headroom_warning():
    result = evaluate({"cpu": "r7-7800x3d", "gpu": "rtx5070", "psu": "rm750e"})
    assert result["power"]["estimated"] == 50 + 120 + 250
    assert levels(result, "psu") == []
    result = evaluate({"cpu": "i7-14700k", "gpu": "rtx5080", "psu": "rm750e"})
    assert "warning" in levels(result, "psu")


def test_unknown_part_reported():
    result = evaluate({"gpu": "rtx9999"})
    assert "error" in levels(result, "gpu")


def test_every_part_has_a_price_and_unique_id():
    seen = set()
    for category, parts in CATALOG.items():
        for part in parts:
            assert part["price"] > 0
            assert part["id"] not in seen
            seen.add(part["id"])


def test_health_endpoints():
    c = client()
    assert c.get("/healthz").status_code == 200
    assert c.get("/readyz").status_code == 200


def test_check_endpoint_validates_input():
    c = client()
    assert c.post("/api/check", json={"parts": "nope"}).status_code == 400
    ok = c.post("/api/check", json={"parts": PRESETS["1440p-gaming"]["parts"]})
    assert ok.status_code == 200 and ok.get_json()["status"] == "ok"


def test_metrics_recorded_but_not_on_app_port():
    from prometheus_client import generate_latest
    c = client()
    c.post("/api/check", json={"parts": {}})
    body = generate_latest().decode()
    assert "pcforge_build_checks_total" in body
    assert "pcforge_http_requests_total" in body
    # /metrics must NOT be served by the app (it lives on METRICS_PORT instead)
    assert c.get("/metrics").status_code == 404


def test_index_shows_deploy_info():
    html = client().get("/").get_data(as_text=True)
    assert "PCForge" in html and "version" in html
