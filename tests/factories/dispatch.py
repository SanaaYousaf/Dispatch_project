import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from .order import OrderFactory

faker = FakerFactory.create()


@register
class DispatchFactory(DjangoModelFactory):
    order = factory.SubFactory(OrderFactory)
    action = factory.sequence(lambda x: 'action{}'.format(x))

    class Meta:
        model = 'dispatch.Dispatch'
