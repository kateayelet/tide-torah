from fastapi import APIRouter
from .endpoints import prayer, torah, practical

api_router = APIRouter()

api_router.include_router(prayer.router, prefix="/prayer", tags=["prayer"])
api_router.include_router(torah.router, prefix="/torah", tags=["torah"])
api_router.include_router(practical.router, prefix="/practical", tags=["practical"])
