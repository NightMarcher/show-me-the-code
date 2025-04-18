from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/now")
async def get_now():
    return datetime.now().isoformat()
