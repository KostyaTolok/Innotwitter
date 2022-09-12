import json

from django.urls import reverse

from users.models import User

endpoint = reverse("users:users-list")


def test_list(admin_api_client, user_data, admin_data):
    response = admin_api_client.get(endpoint)
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 2


def test_retrieve(admin_api_client, user_data, admin_data):
    response = admin_api_client.get(f"{endpoint}{user_data.id}/")
    user = json.loads(response.content)
    assert response.status_code == 200
    assert user.get("username") == user_data.username


def test_register(db, unauthorized_api_client):
    response = unauthorized_api_client.post(f"{endpoint}register/",
                                            data={'username': 'new_user', 'password': 'password',
                                                  'email': 'new@gmail.com'}, format="json")
    new_user = User.objects.filter(username='new_user').first()
    assert response.status_code == 200
    assert new_user is not None


def test_register_exists(user_data, unauthorized_api_client):
    response = unauthorized_api_client.post(f"{endpoint}register/",
                                            data={'username': 'user', 'password': 'password',
                                                  'email': 'user@gmail.com'}, format="json")
    assert response.status_code == 400


def test_login(db, unauthorized_api_client):
    response = unauthorized_api_client.post(f"{endpoint}register/",
                                            data={'username': 'new_user', 'password': 'password',
                                                  'email': 'new@gmail.com'},
                                            format="json")
    assert response.status_code == 200

    response = unauthorized_api_client.post(f"{endpoint}login/",
                                            data={"username": 'new_user', "password": "password"},
                                            format="json")
    assert response.status_code == 200
    assert json.loads(response.content).get("token", None) is not None


def test_login_not_exists(db, unauthorized_api_client):
    response = unauthorized_api_client.post(f"{endpoint}login/",
                                            data={"username": 'new_user', "password": "password"},
                                            format="json")
    assert response.status_code == 404


def test_login_incorrect_password(db, unauthorized_api_client):
    response = unauthorized_api_client.post(f"{endpoint}register/",
                                            data={'username': 'new_user', 'password': 'new_password',
                                                  'email': 'new@gmail.com'}, format="json")
    assert response.status_code == 200

    response = unauthorized_api_client.post(f"{endpoint}login/",
                                            data={"username": 'new_user', "password": "password"},
                                            format="json")
    assert response.status_code == 400
