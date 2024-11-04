from fastapi import APIRouter, HTTPException
import logging

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

logger = logging.getLogger(__name__)


@router.get("")
async def list_users():
    try:
        return {"data": {"users": [{"name": "John Doe", "email": "heribeto@hotmail.com"}]}}
    except Exception as e:
        logger.error(f"Error listing users{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
