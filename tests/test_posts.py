import json

from django.urls import reverse

from posts.models import Post

endpoint = reverse("posts:posts-list")


def test_list(admin_api_client, posts_data):
    response = admin_api_client.get(endpoint)
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 2


def test_retrieve(api_client, posts_data):
    response = api_client.get(f"{endpoint}{posts_data[0].id}/")
    post = json.loads(response.content)
    assert response.status_code == 200
    assert post.get("id") == posts_data[0].id


def test_retrieve_blocked(api_client, posts_data, blocked_page_data):
    response = api_client.get(f"{endpoint}{posts_data[0].id}/")
    assert response.status_code == 403


def test_create(api_client, posts_data, pages_data):
    new_post_info = {"content": "New post",
                     "page": pages_data[0].uuid}
    response = api_client.post(endpoint, data=new_post_info, format="json")
    post = json.loads(response.content)
    assert response.status_code == 201
    assert post.get("content") == new_post_info.get("content")


def test_create_not_owner(api_client, posts_data, pages_data):
    new_post_info = {"content": "New post",
                     "page": pages_data[1].uuid}
    response = api_client.post(endpoint, data=new_post_info, format="json")
    assert response.status_code == 403


def test_create_blocked(api_client, posts_data, pages_data, blocked_page_data):
    new_post_info = {"content": "New post",
                     "page": pages_data[0].uuid}
    response = api_client.post(endpoint, data=new_post_info, format="json")
    assert response.status_code == 403


def test_update(api_client, posts_data, pages_data):
    response = api_client.put(f"{endpoint}{posts_data[0].id}/",
                              data={"page": pages_data[0].uuid, "content": "Updated post"},
                              format="json")
    page = json.loads(response.content)
    assert response.status_code == 200
    assert page.get("content") == "Updated post"


def test_update_not_owner(api_client, posts_data, pages_data):
    response = api_client.put(f"{endpoint}{posts_data[1].id}/",
                              data={"page": pages_data[1].uuid, "content": "Updated post"},
                              format="json")
    assert response.status_code == 403


def test_update_blocked(api_client, posts_data, pages_data, blocked_page_data):
    response = api_client.put(f"{endpoint}{posts_data[0].id}/",
                              data={"page": pages_data[0].uuid, "content": "Updated post"},
                              format="json")
    assert response.status_code == 403


def test_destroy(api_client, posts_data):
    response = api_client.delete(f"{endpoint}{posts_data[0].id}/")
    assert response.status_code == 204


def test_destroy_not_owner(api_client, posts_data):
    response = api_client.delete(f"{endpoint}{posts_data[1].id}/")
    assert response.status_code == 403


def test_destroy_blocked(api_client, posts_data, blocked_page_data):
    response = api_client.delete(f"{endpoint}{posts_data[0].id}/")
    assert response.status_code == 403


def test_change_like_status(api_client, posts_data, user_data):
    response = api_client.post(f"{endpoint}{posts_data[0].id}/change-like/")
    post = Post.objects.filter(id=posts_data[0].id).first()
    assert response.status_code == 200
    assert post.likes.contains(user_data)


def test_change_like_status_blocked(api_client, posts_data, blocked_page_data):
    response = api_client.post(f"{endpoint}{posts_data[0].id}/change-like/")
    assert response.status_code == 403


def test_get_liked_posts(api_client, posts_data, user_data):
    posts_data[0].likes.add(user_data)
    response = api_client.get(f"{endpoint}liked-posts/")
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1


def test_get_news_feed(api_client, posts_data, pages_data, user_data):
    posts_data[0].likes.add(user_data)
    pages_data[1].followers.add(user_data)
    response = api_client.get(f"{endpoint}news-feed/")
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 2

