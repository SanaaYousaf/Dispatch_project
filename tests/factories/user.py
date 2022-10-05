import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

faker = FakerFactory.create()


@register
class UserFactory(DjangoModelFactory):
    username = factory.sequence(lambda x: 'username{}'.format(x))
    password = factory.sequence(lambda x: 'password{}'.format(x))
    email = factory.sequence(lambda x: 'email{}'.format(x))
    is_active = True

    class Meta:
        model = 'dispatch.User'

    @factory.post_generation
    def password(self, create, extracted):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            self.set_password(extracted)
