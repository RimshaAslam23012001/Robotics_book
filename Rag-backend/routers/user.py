from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from middleware.auth import get_current_user
from services.personalization_service import personalization_service
from schemas import GetUserBackgroundResponse, UpdateUserBackgroundResponse
from datetime import datetime

router = APIRouter()


@router.get("/user/background", response_model=GetUserBackgroundResponse)
async def get_user_background(current_user: str = Depends(get_current_user)):
    """
    Get the user's background preferences.
    """
    try:
        user_profile = personalization_service.get_user_background(current_user)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User background not found")

        return GetUserBackgroundResponse(
            userId=user_profile.userId,
            technicalDepth=user_profile.technicalDepth,
            terminologyComplexity=user_profile.terminologyComplexity,
            exampleFocus=user_profile.exampleFocus,
            aiConceptLevel=user_profile.aiConceptLevel,
            createdAt=user_profile.createdAt,
            updatedAt=user_profile.updatedAt
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/user/background", response_model=UpdateUserBackgroundResponse)
async def update_user_background(
    background_data: Dict[str, Any],
    current_user: str = Depends(get_current_user)
):
    """
    Update the user's background preferences.
    """
    try:
        updated_profile = personalization_service.update_user_background(
            current_user,
            background_data
        )

        if not updated_profile:
            raise HTTPException(status_code=400, detail="Invalid background data")

        return UpdateUserBackgroundResponse(
            userId=updated_profile.userId,
            technicalDepth=updated_profile.technicalDepth,
            terminologyComplexity=updated_profile.terminologyComplexity,
            exampleFocus=updated_profile.exampleFocus,
            aiConceptLevel=updated_profile.aiConceptLevel,
            updatedAt=updated_profile.updatedAt
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")