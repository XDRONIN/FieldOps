from fastapi import APIRouter

from app.api.v1.endpoints import auth, admin, requests, tasks, dashboards

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(requests.router, prefix="/requests", tags=["requests"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(dashboards.router, prefix="/dashboard", tags=["dashboard"])
