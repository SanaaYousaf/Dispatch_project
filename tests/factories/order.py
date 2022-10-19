import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register
from .user import UserFactory

faker = FakerFactory.create()


@register
class OrderFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    shipper = factory.sequence(lambda x: 'shipper{}'.format(x))

    class Meta:
        model = 'dispatch.Order'
