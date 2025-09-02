import datetime

import pydantic

from db.models import User

class UserBase(pydantic.BaseModel):
    """Base User schema."""

    username: str = pydantic.Field(
        min_length=User.USERNAME_MIN_LEN,
        max_length=User.USERNAME_MAX_LEN,
    )
    email: pydantic.EmailStr = pydantic.Field(
        min_length=User.EMAIL_MIN_LEN,
        max_length=User.EMAIL_MAX_LEN,
    )


class UserCreate(UserBase):
    """User schema to create instance."""

    password: str


class UserOut(UserBase):
    """User schema for db instances."""

    model_config = pydantic.ConfigDict(
        from_attributes = True,
    )
    id: int
    created: datetime.datetime
    modified: datetime.datetime
