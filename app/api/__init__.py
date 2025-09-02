from fastapi import APIRouter

from api.users.rest import user_router
from api.resumes.rest import resume_router
from .views import view_router

router = APIRouter()
router.include_router(
    user_router,
    prefix="/api/v1/users",
    tags=[
        "User",
    ],
)
router.include_router(
    resume_router,
    prefix="/api/v1/resumes",
    tags=[
        "Resumes",
    ],
)
router.include_router(
    view_router,
)

__all__ = [
    "router",
]
