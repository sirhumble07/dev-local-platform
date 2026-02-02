import sys
import pytest

# Some systems (Python 3.14 as of this workspace) have an incompatibility
# between httpx/httpcore and the typing module which causes collection errors.
# Skip tests on those runtimes and run on Python 3.11 in CI for reproducibility.
pytestmark = pytest.mark.skipif(sys.version_info >= (3, 14), reason="httpx/httpcore incompatible with Python 3.14; run tests with Python 3.11")


def get_client():
    # Import TestClient and app lazily to avoid importing httpx at module-import time
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)


def test_health():
    client = get_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_version_from_env(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "9.9.9-test")
    # reload app module to pick up env var
    import importlib
    import main as m
    importlib.reload(m)
    from fastapi.testclient import TestClient
    client = TestClient(m.app)
    r = client.get("/version")
    assert r.status_code == 200
    assert r.json()["version"] == "9.9.9-test"


def test_metrics_present():
    client = get_client()
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"http_requests_total" in r.content
