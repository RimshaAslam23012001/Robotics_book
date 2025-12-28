from fastapi import APIRouter, Depends, HTTPException
from middleware.auth import get_current_user
from services.translation_service import translation_service
from schemas import TranslateChapterResponse

router = APIRouter()


@router.get("/chapter/{chapter_id}/translate/urdu", response_model=TranslateChapterResponse)
async def translate_chapter_to_urdu(
    chapter_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Translate a chapter to Urdu based on user authentication.
    """
    try:
        result = translation_service.translate_chapter_to_urdu(
            current_user,
            chapter_id
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to translate chapter to Urdu"
            )

        return TranslateChapterResponse(
            chapterId=result["chapterId"],
            translatedContent=result["translatedContent"],
            processingTime=result["processingTime"],
            translationQuality=result["translationQuality"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")