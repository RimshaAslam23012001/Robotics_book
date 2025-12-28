from fastapi import APIRouter, Depends, HTTPException
from middleware.auth import get_current_user
from services.translation_service import translation_service
from schemas import GetChapterResponse

router = APIRouter()


@router.get("/chapter/{chapter_id}", response_model=GetChapterResponse)
async def get_chapter(
    chapter_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Get the original chapter content.
    """
    try:
        chapter_data = translation_service.get_chapter(chapter_id)
        if not chapter_data:
            raise HTTPException(status_code=404, detail="Chapter not found")

        return GetChapterResponse(
            chapterId=chapter_data["chapterId"],
            title=chapter_data["title"],
            slug=chapter_data["slug"],
            originalContent=chapter_data["originalContent"],
            metadata=chapter_data["metadata"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")