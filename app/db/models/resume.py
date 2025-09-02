from tortoise import fields
from tortoise.fields.base import OnDelete
from tortoise.validators import MinLengthValidator, MaxLengthValidator

from db.models.base import BaseModel

class Resume(BaseModel):
    """Represent Resume in db."""

    TITLE_MIN_LEN = 3
    TITLE_MAX_LEN = 120
    CONTENT_MIN_LEN = 10
    CONTENT_MAX_LEN = 2000

    title = fields.CharField(
        max_length=TITLE_MAX_LEN,
        validators=[
            MinLengthValidator(TITLE_MIN_LEN),
            MaxLengthValidator(TITLE_MAX_LEN),
        ],
    )
    content = fields.TextField(
        max_length=CONTENT_MAX_LEN,
        validators=[
            MinLengthValidator(CONTENT_MIN_LEN),
            MaxLengthValidator(CONTENT_MAX_LEN),
        ],
    )
    user = fields.ForeignKeyField(
        model_name="server.User",
        related_name="tasks",
        on_delete=OnDelete.CASCADE,
    )