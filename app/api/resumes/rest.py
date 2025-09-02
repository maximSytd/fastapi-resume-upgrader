from fastapi_babel import _
from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from db import schemas
from db.models import User, Resume
from dependencies.auth import get_current_user
from services.resume_upgrade import (
    ResumeContentLengthError,
    improve_resume_content,
)

resume_router = APIRouter()

RESUME_NOT_FOUND_MESSAGE = "Resume not found"

@resume_router.get("", response_model=Page[schemas.ResumeOut])
async def list_resumes(current_user: User = Depends(get_current_user)):
    """List all resumes for user."""
    return await paginate(Resume.filter(user=current_user))


@resume_router.get(
    "/{resume_id}",
    response_model=schemas.ResumeOut,
)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
):
    """Get a specific resume (for user)."""
    try:
        return await Resume.get(
            id=resume_id,
            user=current_user,
        )
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=_(RESUME_NOT_FOUND_MESSAGE),
        )


@resume_router.post(
    "",
    response_model=schemas.ResumeOut,
    status_code=HTTP_201_CREATED,
)
async def create_resume(
    resume_data: schemas.ResumeCreate,
    current_user: User = Depends(get_current_user),
):
    """Create new resume (for user)."""
    return await Resume.create(
        title=resume_data.title,
        content=resume_data.content,
        user=current_user,
    )


@resume_router.put("/{resume_id}", response_model=schemas.ResumeOut)
async def update_resume(
    resume_id: int,
    resume_data: schemas.ResumeUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update existing resume (for user)."""
    try:
        resume = await Resume.get(
            id=resume_id,
            user=current_user,
        )
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=_(RESUME_NOT_FOUND_MESSAGE),
        )

    resume.title = resume_data.title
    resume.content = resume_data.content

    await resume.save()
    return resume


@resume_router.delete("/{resume_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
):
    """Delete a resume (for user)."""
    deleted_count = await Resume.filter(
        id=resume_id,
        user=current_user,
    ).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=_(RESUME_NOT_FOUND_MESSAGE),
        )


@resume_router.post("/{resume_id}/improve", response_model=schemas.ResumeOut)
async def improve_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
):
    """Improve existing resume content with ai (for user)."""
    try:
        resume = await Resume.get(
            id=resume_id,
            user=current_user,
        )
        resume.content = improve_resume_content(resume.content)
        await resume.save()
        return resume
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=_(RESUME_NOT_FOUND_MESSAGE),
        )
    except ResumeContentLengthError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=_(str(error)),
        )
