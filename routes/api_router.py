from fastapi import APIRouter
from .analytics.analytics_router import router as analytics_router
from .scanner.scanner_router import router as scanner_router
from .credentials.credentials_router import router as credentials_router

router = APIRouter(prefix="/api/v1", tags=["API v1"])

routers = (
    analytics_router,
    scanner_router,
    credentials_router,
)

for i in routers:
    router.include_router(i)
