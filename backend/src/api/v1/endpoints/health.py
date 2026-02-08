from fastapi import APIRouter
from typing import Dict

router = APIRouter(tags=["health"])

@router.get("/health", response_model=Dict[str, str])
async def health_check():
    """
    Health check endpoint to verify the application is running
    """
    return {"status": "healthy", "message": "Todo application is running correctly"}