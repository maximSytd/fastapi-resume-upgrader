from tortoise import fields
from tortoise.validators import MinLengthValidator, MaxLengthValidator

from db.models.base import BaseModel

class User(BaseModel):
    """Represent User in db."""

    USERNAME_MIN_LEN = 3
    USERNAME_MAX_LEN = 64
    EMAIL_MIN_LEN = 3
    EMAIL_MAX_LEN = 320

    username = fields.CharField(
        max_length=USERNAME_MAX_LEN,
        unique=True,
        validators=[
            MinLengthValidator(USERNAME_MIN_LEN),
            MaxLengthValidator(USERNAME_MAX_LEN),
        ],
    )
    email = fields.CharField(
        max_length=EMAIL_MAX_LEN,
        unique=True,
        validators=[
            MinLengthValidator(EMAIL_MIN_LEN),
            MaxLengthValidator(EMAIL_MAX_LEN),
        ],
    )
    password_hash = fields.CharField(
        max_length=128,
    )
