import json

from django.urls import reverse
from rest_framework import status

from users.models import User

endpoint = reverse("users:users-list")


def test_list_200(admin_api_client, user_data, admin_data):
    response = admin_api_client.get(reverse("users:users-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(json.loads(response.content)) == 2


def test_retrieve_200(admin_api_client, user_data, admin_data):
    response = admin_api_client.get(reverse("users:users-detail", args=[user_data.id]))
    user = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert user.get("username") == user_data.username


def test_register_200(db, unauthorized_api_client):
    response = unauthorized_api_client.post(reverse("users:users-register"),
                                            data={'username': 'new_user', 'password': 'password',
                                                  'email': 'new@gmail.com'}, format="json")
    new_user = User.objects.filter(username='new_user').first()
    assert response.status_code == status.HTTP_200_OK
    assert new_user is not None


def test_register_exists_400(user_data, unauthorized_api_client):
    response = unauthorized_api_client.post(reverse("users:users-register"),
                                            data={'username': 'user', 'password': 'password',
                                                  'email': 'user@gmail.com'}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_200(db, unauthorized_api_client):
    response = unauthorized_api_client.post(reverse("users:users-register"),
                                            data={'username': 'new_user', 'password': 'password',
                                                  'email': 'new@gmail.com'},
                                            format="json")
    assert response.status_code == status.HTTP_200_OK

    response = unauthorized_api_client.post(reverse("users:users-login"),
                                            data={"username": 'new_user', "password": "password"},
                                            format="json")
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content).get("token", None) is not None


def test_login_not_exists_404(db, unauthorized_api_client):
    response = unauthorized_api_client.post(reverse("users:users-login"),
                                            data={"username": 'new_user', "password": "password"},
                                            format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_login_incorrect_password_400(db, unauthorized_api_client):
    response = unauthorized_api_client.post(reverse("users:users-register"),
                                            data={'username': 'new_user', 'password': 'new_password',
                                                  'email': 'new@gmail.com'}, format="json")
    assert response.status_code == status.HTTP_200_OK

    response = unauthorized_api_client.post(reverse("users:users-login"),
                                            data={"username": 'new_user', "password": "password"},
                                            format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
