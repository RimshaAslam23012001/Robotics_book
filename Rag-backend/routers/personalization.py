from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from middleware.auth import get_current_user
from services.personalization_service import personalization_service
from schemas import PersonalizeChapterResponse

router = APIRouter()


@router.get("/chapter/{chapter_id}/personalize", response_model=PersonalizeChapterResponse)
async def personalize_chapter(
    chapter_id: str,
    learning_goal: Optional[str] = None,
    current_user: str = Depends(get_current_user)
):
    """
    Personalize a chapter based on user background.
    """
    try:
        result = personalization_service.personalize_chapter(
            current_user,
            chapter_id,
            learning_goal
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to personalize chapter content"
            )

        return PersonalizeChapterResponse(
            chapterId=result["chapterId"],
            personalizedContent=result["personalizedContent"],
            processingTime=result["processingTime"],
            userBackgroundApplied=result["userBackgroundApplied"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")