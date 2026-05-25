from fastapi import FastAPI

from prometheus_fastapi_instrumentator import (
    Instrumentator,
)

from app.api.v1.api import api_router
from slowapi.errors import (
    RateLimitExceeded,
)

from slowapi.middleware import (
    SlowAPIMiddleware,
)

from slowapi import _rate_limit_exceeded_handler
from app.core.rate_limit import (
    limiter,
)


app = FastAPI(
    title="CodeRank",
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

app.add_middleware(
    SlowAPIMiddleware,
)

Instrumentator().instrument(app).expose(app)


@app.get("/health")
async def health():
    return {
        "status": "ok",
    }


app.include_router(
    api_router,
    prefix="/api/v1",
)