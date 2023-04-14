from urllib.request import Request

from fastapi import FastAPI
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

REQUEST_COUNT = Counter("request_count", "Total count of requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["method", "endpoint"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    with REQUEST_LATENCY.labels(method, endpoint).time():
        response = await call_next(request)
        http_status = response.status_code
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=http_status).inc()
    return response
