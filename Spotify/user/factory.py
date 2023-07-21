import factory
from faker import Faker
from factory.faker import Faker as FactoryFaker
from factory import LazyFunction, post_generation, SubFactory
from .models import User
import datetime

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["email"]

    email = FactoryFaker("email")
    username = FactoryFaker("name")
    first_name = FactoryFaker("first_name")
    last_name = FactoryFaker("last_name")
    profile_photo = factory.django.ImageField(format="jpeg")

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = (
            extracted
            if extracted
            else FactoryFaker(
                "password",
                length=42,
                special_chars=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)
