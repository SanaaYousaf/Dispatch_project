from django.urls import reverse
from rest_framework import status


def test_signup_user(rest_client, mailoutbox):
    data = {
        "username": "sana",
        'email': 'sana123@gmail.com',
        'password': '123456'}
    # client = rest_client()
    response = rest_client.post(reverse('register'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['username'] == data['username']
    assert len(mailoutbox) == 1
    x = mailoutbox[0].body.split(' ')
    data = {
        "email": "sana123@gmail.com",
        "otp": x[3],
    }
    response = rest_client.post(reverse('verify'), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 'account verified'


def test_login_user(rest_client, user_factory):
    user = user_factory(email='testuser@gmail.com', password='test1234')
    data = {
        "email": user.email,
        "password": 'test1234'
    }
    response = rest_client.post(reverse('login'), data=data)
    assert response.status_code == status.HTTP_200_OK
