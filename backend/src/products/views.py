"""
Views
"""
from fastapi import APIRouter

from .custom_views.user_access_views import router as user_router
from .custom_views.query_token_views import router as token_router

router = APIRouter(prefix="/product", tags=["Products"])
router.include_router(user_router)
router.include_router(token_router)
