import os
import sys
import time
import logging
from typing import Callable

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Basic logging to stdout
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("app")

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency seconds",
    ["method", "endpoint"],
)

app = FastAPI(title="DevOps Local Platform - FastAPI App", version=APP_VERSION)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next: Callable):
    start = time.time()
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception:  # capture exceptions as 500s
        status_code = 500
        logger.exception("Unhandled exception")
        raise
    finally:
        resp_time = time.time() - start
        endpoint = request.url.path
        REQUEST_LATENCY.labels(request.method, endpoint).observe(resp_time)
        REQUEST_COUNT.labels(request.method, endpoint, str(status_code)).inc()


@app.get("/health", tags=["health"])
async def health():
    """Simple health endpoint used in health checks."""
    return {"status": "ok"}


@app.get("/version", tags=["meta"])
async def version():
    """Return application version from environment (container-friendly)."""
    return {"version": APP_VERSION}


@app.get("/metrics", include_in_schema=False)
async def metrics():
    """Expose Prometheus metrics."""
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get("/", tags=["root"])
async def root():
    return {"message": "DevOps Local Platform - FastAPI app is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("APP_PORT", 8000)), log_level="info")
