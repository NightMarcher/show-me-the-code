from datetime import datetime
from logging import getLogger

from fastapi import APIRouter

logger = getLogger(__name__)

router = APIRouter()


@router.get("/now")
async def get_now():
    now = datetime.now().isoformat()
    logger.info(f"Current time: {now}")
    return now
