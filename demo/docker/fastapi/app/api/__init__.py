from fastapi import APIRouter

from . import base

api_router = APIRouter()

api_router.include_router(base.router, prefix="/base", tags=["Base"])
