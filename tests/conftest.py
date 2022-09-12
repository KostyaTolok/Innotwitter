from datetime import timedelta, datetime

import pytest
from rest_framework.test import APIClient

from pages.models import Page, Tag
from posts.models import Post
from users.models import User, Roles
from users.services import generate_token


@pytest.fixture
def api_client():
    access_token = generate_token("user", Roles.USER, timedelta(minutes=5))
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=access_token)
    return api_client


@pytest.fixture
def second_api_client():
    access_token = generate_token("user2", Roles.USER, timedelta(minutes=5))
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=access_token)
    return api_client


@pytest.fixture
def admin_api_client():
    access_token = generate_token("admin", Roles.ADMIN, timedelta(minutes=5))
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=access_token)
    return api_client


@pytest.fixture
def unauthorized_api_client():
    return APIClient()


@pytest.fixture
def user_data(db):
    user = User.objects.create(id=1, username="user", email="user@gmail.com", password="user")
    return user


@pytest.fixture
def admin_data(db):
    user = User.objects.create(id=2, username="admin", email="admin@gmail.com", password="admin", role=Roles.ADMIN)
    return user


@pytest.fixture
def second_user_data(db):
    user = User.objects.create(id=3, username="user2", email="user2@gmail.com", password="password")
    return user


@pytest.fixture
def tags_data(db):
    tag1 = Tag.objects.create(id=1, name="tag 1")
    tag2 = Tag.objects.create(id=2, name="tag 2")
    return [tag1, tag2]


@pytest.fixture
def pages_data(db, tags_data, user_data, admin_data):
    page1 = Page.objects.create(uuid="ff55980c-301e-11ed-a261-0242ac120002", name="Page 1", owner=user_data)
    page2 = Page.objects.create(uuid="0c1469e2-301f-11ed-a261-0242ac120002", name="Page 2", owner=admin_data)

    page1.tags.add(tags_data[0])
    page2.tags.add(tags_data[1])

    page1.follow_requests.add(admin_data)
    return [page1, page2]


@pytest.fixture
def blocked_page_data(db, pages_data):
    pages_data[0].unblock_date = datetime.utcnow() + timedelta(days=1)
    pages_data[0].is_blocked_permanently = True
    pages_data[0].save()
    return pages_data[0]


@pytest.fixture
def private_page_data(db, pages_data):
    pages_data[0].is_private = True
    pages_data[0].save()
    return pages_data[0]


@pytest.fixture
def posts_data(db, pages_data):
    post1 = Post.objects.create(content="Post 1", page=pages_data[0])
    post2 = Post.objects.create(content="Post 2", page=pages_data[1])

    return [post1, post2]
