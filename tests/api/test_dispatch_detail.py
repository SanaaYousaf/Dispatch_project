from django.urls import reverse
from rest_framework import status


def test_get_dispatch(user_factory, order_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    order = order_factory(user=user)
    dispatch = dispatch_factory(order=order)
    data = {
         'action': 'D'
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse("dispatch_detail", kwargs={'pk': dispatch.id}), data=data, format='json')
    assert response.json()['action'] == data['action']
    assert response.json()['id'] == dispatch.id


def test_get_dispatch_by_other_user(user_factory, order_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    user2 = user_factory()
    order = order_factory(user=user)
    dispatch = dispatch_factory(order=order)
    data = {
        'action': 'D'
    }
    client = authed_token_client_generator(user2)
    response = client.patch(reverse("dispatch_detail", kwargs={'pk': dispatch.id}), data=data, format='json')
    assert response.json()['detail'] == "You do not have permission to perform this action."


def test_delete_dispatch(user_factory, order_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    order = order_factory(user=user)
    dispatch = dispatch_factory(order=order)
    client = authed_token_client_generator(user)
    response = client.delete(reverse("dispatch_detail", kwargs={'pk': dispatch.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_dispatch_by_other_user(user_factory, order_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    user2 = user_factory()
    order = order_factory(user=user)
    dispatch = dispatch_factory(order=order)
    client = authed_token_client_generator(user2)
    response = client.delete(reverse("dispatch_detail", kwargs={'pk': dispatch.id}))
    assert response.json()['detail'] == "You do not have permission to perform this action."
    assert response.status_code == status.HTTP_403_FORBIDDEN

