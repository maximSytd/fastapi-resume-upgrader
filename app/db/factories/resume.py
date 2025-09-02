import factory
import factory.fuzzy
from async_factory_boy.factory.tortoise import AsyncTortoiseFactory

from db.models import Resume
from db.factories import AsyncUserFactory


class AsyncResumeFactory(AsyncTortoiseFactory):
    """Async factory to generate test Resume instance."""

    title = factory.Faker("job")
    content = factory.Faker("paragraph")
    user = factory.SubFactory(AsyncUserFactory)

    class Meta:
        model = Resume
