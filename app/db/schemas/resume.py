import datetime

import pydantic

from db.models import Resume


class ResumeBase(pydantic.BaseModel):
    """Base Resume schema."""

    title: str = pydantic.Field(
        min_length=Resume.TITLE_MIN_LEN,
        max_length=Resume.TITLE_MAX_LEN,
    )
    content: str = pydantic.Field(
        min_length=Resume.CONTENT_MIN_LEN,
        max_length=Resume.CONTENT_MAX_LEN,
    )

class ResumeCreate(ResumeBase):
    """Resume schema to create instance."""


class ResumeUpdate(ResumeBase):
    """Resume schema to update instance."""


class ResumeOut(ResumeBase):
    """Resume schema for db instances."""

    model_config = pydantic.ConfigDict(
        from_attributes = True,
    )
    id: int
    created: datetime.datetime
    modified: datetime.datetime
