from fastapi import APIRouter
from app.api.v1.endpoints import hands

api_router = APIRouter()
api_router.include_router(hands.router, prefix="/hands", tags=["hands"])