from fastapi import APIRouter
from app.api.v1.endpoints import employee, leave, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(employee.router, prefix="/employees", tags=["employees"])
api_router.include_router(leave.router, prefix="/leaves", tags=["leaves"])