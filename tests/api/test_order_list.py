from django.urls import reverse
from rest_framework import status

from dispatch.models import Order


def test_get_order(user_factory, order_factory, authed_token_client_generator):
    user = user_factory()
    order = order_factory(user=user)
    client = authed_token_client_generator(user)
    response = client.get(reverse('dispatch-order'))
    assert response.json()[0]['id'] == order.id
    assert response.json()[0]['user'] == user.id


def test_get_order_by_other_user(user_factory, order_factory, authed_token_client_generator):
    user = user_factory()
    user2 = user_factory()
    order = order_factory(user=user)
    client = authed_token_client_generator(user2)
    response = client.get(reverse('dispatch-order'))
    assert len(response.json()) == 0
    assert Order.objects.count() == 1


def test_create_order(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {
        "user": user.id,
        "shipper": "test_shipper"
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('dispatch-order'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['user'] == data["user"]
    assert response.json()['user'] == user.id


def test_create_order_by_other_user(user_factory, authed_token_client_generator):
    user = user_factory()
    user2 = user_factory()
    data = {
        "user": user.id,
        "shipper": "test_shipper"
    }
    client = authed_token_client_generator(user2)
    response = client.post(reverse('dispatch-order'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == 'enter a valid user'

