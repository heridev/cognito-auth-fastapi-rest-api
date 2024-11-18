from fastapi import APIRouter, HTTPException, Depends
import logging
from app.services.aws.cognito_service import CognitoService
from app.config import settings
from app.models.users import UserProfile
from typing import Optional


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

logger = logging.getLogger(__name__)


def require_auth():
    """Dependency for protected endpoints"""
    return Depends(cognito_service.validate_token)


@router.get("")
async def list_users():
    try:
        return {"data": {"users": [{"name": "Heriberto Perez", "email": "heribertoperez@email.com"}]}}
    except Exception as e:
        logger.error(f"Error listing users{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

cognito_service = CognitoService(settings)


# For more customizations
# @router.get(
#     "/me",
#     response_model=UserProfile,
#     responses={
#         200: {
#             "description": "Successful response",
#             "content": {
#                 "application/json": {
#                     "example": {
#                         "user_id": "test",
#                         "email": "example@email.com",
#                         "name": "Test User"
#                     }
#                 }
#             }
#         },
#         401: {
#             "description": "Invalid or expired token",
#             "content": {
#                 "application/json": {
#                     "example": {"detail": "Invalid token or expired token"}
#                 }
#             }
#         }
#     }
# )
@router.get("/me", response_model=UserProfile)
async def get_current_user(token: Optional[dict] = Depends(cognito_service.validate_token)):
    """Example protected endpoint that returns user claims"""
    print('token', token)

    return {
        "user_id": 'test',
        "email": 'another',
        "name": 'name'
    }


@router.get("/me/alternative", response_model=UserProfile)
async def get_current_user(token: dict = require_auth()):
    """Example protected endpoint that returns user claims"""
    return {
        "user_id": 'test',
        "email": 'another',
        "name": 'name'
    }
