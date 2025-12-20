from fastapi import APIRouter
from datetime import datetime
from typing import Dict

router = APIRouter()


@router.get("/status", tags=["status"])
async def get_status() -> Dict:
    """
    Health check endpoint to verify the service is running
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }