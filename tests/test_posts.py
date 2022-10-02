import json

from django.urls import reverse
from rest_framework import status

from posts.models import Post


def test_list_200(admin_api_client, posts_data):
    response = admin_api_client.get(reverse("posts:posts-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(json.loads(response.content)) == 2


def test_retrieve_200(api_client, posts_data):
    response = api_client.get(reverse("posts:posts-detail", args=[posts_data[0].id]))
    post = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert post.get("id") == posts_data[0].id


def test_retrieve_blocked_403(api_client, posts_data, blocked_page_data):
    response = api_client.get(reverse("posts:posts-detail", args=[posts_data[0].id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_201(api_client, posts_data, pages_data):
    new_post_info = {"content": "New post",
                     "page": pages_data[0].uuid}
    response = api_client.post(reverse("posts:posts-list"), data=new_post_info, format="json")
    post = json.loads(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert post.get("content") == new_post_info.get("content")


def test_create_not_owner_403(api_client, posts_data, pages_data):
    new_post_info = {"content": "New post",
                     "page": pages_data[1].uuid}
    response = api_client.post(reverse("posts:posts-list"), data=new_post_info, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_blocked_403(api_client, posts_data, pages_data, blocked_page_data):
    new_post_info = {"content": "New post",
                     "page": pages_data[0].uuid}
    response = api_client.post(reverse("posts:posts-list"), data=new_post_info, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_200(api_client, posts_data, pages_data):
    response = api_client.put(reverse("posts:posts-detail", args=[posts_data[0].id]),
                              data={"page": pages_data[0].uuid, "content": "Updated post"},
                              format="json")
    page = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert page.get("content") == "Updated post"


def test_update_not_owner_403(api_client, posts_data, pages_data):
    response = api_client.put(reverse("posts:posts-detail", args=[posts_data[1].id]),
                              data={"page": pages_data[1].uuid, "content": "Updated post"},
                              format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_blocked_403(api_client, posts_data, pages_data, blocked_page_data):
    response = api_client.put(reverse("posts:posts-detail", args=[posts_data[0].id]),
                              data={"page": pages_data[0].uuid, "content": "Updated post"},
                              format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_destroy_204(api_client, posts_data):
    response = api_client.delete(reverse("posts:posts-detail", args=[posts_data[0].id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_destroy_not_owner_403(api_client, posts_data):
    response = api_client.delete(reverse("posts:posts-detail", args=[posts_data[1].id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_destroy_blocked_403(api_client, posts_data, blocked_page_data):
    response = api_client.delete(reverse("posts:posts-detail", args=[posts_data[0].id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_change_like_status_200(api_client, posts_data, user_data):
    response = api_client.post(reverse("posts:posts-change_like_status", args=[posts_data[0].id]))
    post = Post.objects.filter(id=posts_data[0].id).first()
    assert response.status_code == status.HTTP_200_OK
    assert post.likes.contains(user_data)


def test_change_like_status_blocked_403(api_client, posts_data, blocked_page_data):
    response = api_client.post(reverse("posts:posts-change_like_status", args=[posts_data[0].id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_liked_posts_200(api_client, posts_data, user_data):
    posts_data[0].likes.add(user_data)
    response = api_client.get(reverse("posts:posts-get_liked_posts"))
    assert response.status_code == status.HTTP_200_OK
    assert len(json.loads(response.content)) == 1


def test_get_news_feed_200(api_client, posts_data, pages_data, user_data):
    posts_data[0].likes.add(user_data)
    pages_data[1].followers.add(user_data)
    response = api_client.get(reverse("posts:posts-get_news_feed"))
    assert response.status_code == status.HTTP_200_OK
    assert len(json.loads(response.content)) == 2
