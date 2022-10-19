from django.urls import reverse
from rest_framework import status

from dispatch.models import Dispatch


def test_get_dispatch(user_factory, order_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    order = order_factory(user=user)
    dispatch = dispatch_factory(order=order)
    client = authed_token_client_generator(user)
    response = client.get(reverse('dispatch'))
    assert response.json()[0]['id'] == dispatch.id
    assert order.user_id == user.id


def test_get_dispatch_by_other_user(user_factory, order_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    user2 = user_factory()
    order = order_factory(user=user)
    dispatch = dispatch_factory(order=order)
    client = authed_token_client_generator(user2)
    response = client.get(reverse('dispatch-order'))
    assert len(response.json()) == 0
    assert Dispatch.objects.count() == 1


def test_create_dispatch(user_factory, order_factory, authed_token_client_generator):
    user = user_factory()
    order = order_factory(user=user)
    client = authed_token_client_generator(user)
    data = {
        "order": order.id
    }
    response = client.post(reverse('dispatch'), data=data)
    assert response.json()['order'] == data["order"]
    assert order.user_id == user.id
    assert response.status_code == status.HTTP_201_CREATED


def test_create_dispatch_by_other_user(user_factory, order_factory, authed_token_client_generator):
    user = user_factory()
    user2 = user_factory()
    order = order_factory(user=user2)
    client = authed_token_client_generator(user)
    data = {
        "order": order.id
    }
    response = client.post(reverse('dispatch'), data=data)
    assert response.json() == 'enter a valid order'
    assert response.status_code == status.HTTP_400_BAD_REQUEST
