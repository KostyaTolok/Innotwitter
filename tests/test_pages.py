import json
from datetime import datetime, timedelta

from django.urls import reverse

from pages.models import Page

endpoint = reverse("pages:pages-list")


def test_list(api_client, pages_data):
    response = api_client.get(endpoint)
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 2


def test_retrieve(api_client, pages_data):
    response = api_client.get(f"{endpoint}{pages_data[0].uuid}/")
    page = json.loads(response.content)
    assert response.status_code == 200
    assert page.get("name") == pages_data[0].name


def test_retrieve_blocked(api_client, blocked_page_data):
    response = api_client.get(f"{endpoint}{blocked_page_data.uuid}/")
    assert response.status_code == 403


def test_retrieve_blocked_admin(admin_api_client, blocked_page_data):
    response = admin_api_client.get(f"{endpoint}{blocked_page_data.uuid}/")
    page = json.loads(response.content)
    assert response.status_code == 200
    assert page.get("name") == blocked_page_data.name


def test_retrieve_private(second_api_client, private_page_data, second_user_data):
    response = second_api_client.get(f"{endpoint}{private_page_data.uuid}/")
    assert response.status_code == 403


def test_retrieve_private_owner(api_client, private_page_data):
    response = api_client.get(f"{endpoint}{private_page_data.uuid}/")
    page = json.loads(response.content)
    assert response.status_code == 200
    assert page.get("name") == private_page_data.name


def test_retrieve_private_admin(admin_api_client, private_page_data):
    response = admin_api_client.get(f"{endpoint}{private_page_data.uuid}/")
    page = json.loads(response.content)
    assert response.status_code == 200
    assert page.get("name") == private_page_data.name


def test_create(api_client, pages_data):
    new_page_info = {"name": "New page",
                     "image_path": "http://127.0.0.1:8000/image",
                     "tags": [1]}
    response = api_client.post(endpoint, data=new_page_info, format="json")
    page = json.loads(response.content)
    assert response.status_code == 201
    assert page.get("name") == new_page_info.get("name")


def test_update(api_client, pages_data):
    response = api_client.put(f"{endpoint}{pages_data[0].uuid}/", data={"name": "Updated page", "tags": [1]},
                              format="json")
    page = json.loads(response.content)
    assert response.status_code == 200
    assert page.get("name") == "Updated page"


def test_update_not_owner(api_client, pages_data):
    response = api_client.put(f"{endpoint}{pages_data[1].uuid}/",
                              data={"name": "Updated page", "tags": [1]}, format="json")
    assert response.status_code == 403


def test_destroy(api_client, pages_data):
    response = api_client.delete(f"{endpoint}{pages_data[0].uuid}/")
    assert response.status_code == 204


def test_destroy_not_owner(api_client, pages_data):
    response = api_client.delete(f"{endpoint}{pages_data[1].uuid}/")
    assert response.status_code == 403


def test_follow(api_client, pages_data, user_data):
    response = api_client.post(f"{endpoint}{pages_data[1].uuid}/follow/")
    assert response.status_code == 200
    assert pages_data[1].followers.contains(user_data)


def test_follow_private(api_client, pages_data, user_data):
    pages_data[1].is_private = True
    pages_data[1].save()
    response = api_client.post(f"{endpoint}{pages_data[1].uuid}/follow/")
    assert response.status_code == 200
    assert pages_data[1].follow_requests.contains(user_data)


def test_follow_owner(api_client, pages_data):
    response = api_client.post(f"{endpoint}{pages_data[0].uuid}/follow/")
    assert response.status_code == 403


def test_follow_already_follows(api_client, pages_data, user_data):
    pages_data[1].followers.add(user_data)
    response = api_client.post(f"{endpoint}{pages_data[1].uuid}/follow/")
    assert response.status_code == 400
    assert response.data == "User already follows this page"


def test_follow_already_sent_request(api_client, pages_data, user_data):
    pages_data[1].follow_requests.add(user_data)
    response = api_client.post(f"{endpoint}{pages_data[1].uuid}/follow/")
    assert response.status_code == 400
    assert response.data == "User already sent follow request to this page"


def test_unfollow(api_client, pages_data, user_data):
    pages_data[1].followers.add(user_data)
    response = api_client.post(f"{endpoint}{pages_data[1].uuid}/unfollow/")
    assert response.status_code == 200
    assert not pages_data[1].followers.contains(user_data)


def test_unfollow_doesnt_follow(api_client, pages_data, user_data):
    response = api_client.post(f"{endpoint}{pages_data[1].uuid}/unfollow/")
    assert response.status_code == 400
    assert response.data == "User doesn't follow this page"


def test_get_follow_requests(api_client, pages_data):
    response = api_client.get(f"{endpoint}{pages_data[0].uuid}/follow-requests/")
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1


def test_accept_follow_request(api_client, pages_data, admin_data):
    response = api_client.post(f"{endpoint}{pages_data[0].uuid}/accept-follow/", data={"user_id": 2}, format="json")
    assert response.status_code == 200
    assert pages_data[0].followers.contains(admin_data)


def test_accept_follow_request_user_blocked(api_client, pages_data, admin_data):
    admin_data.is_blocked = True
    admin_data.save()
    response = api_client.post(f"{endpoint}{pages_data[0].uuid}/accept-follow/", data={"user_id": 2}, format="json")
    assert response.status_code == 400
    assert response.data == "User is blocked"


def test_accept_follow_request_no_follow_request(api_client, pages_data, admin_data):
    pages_data[0].follow_requests.remove(admin_data)
    response = api_client.post(f"{endpoint}{pages_data[0].uuid}/accept-follow/", data={"user_id": 2}, format="json")
    assert response.status_code == 400
    assert response.data == "User didn't send follow request"


def test_accept_follow_request_no_user_id(api_client, pages_data, admin_data):
    response = api_client.post(f"{endpoint}{pages_data[0].uuid}/accept-follow/", format="json")
    assert response.status_code == 400


def test_accept_all_follow_requests(api_client, pages_data, admin_data):
    response = api_client.post(f"{endpoint}{pages_data[0].uuid}/accept-all-follows/")
    assert response.status_code == 200
    assert pages_data[0].followers.contains(admin_data)


def test_block_page(admin_api_client, pages_data):
    unblock_date = (datetime.utcnow() + timedelta(days=1)).strftime("%d.%m.%Y %H:%M")
    response = admin_api_client.patch(f"{endpoint}{pages_data[0].uuid}/block-page/",
                                      data={'unblock_date': unblock_date},
                                      format="json")
    page = Page.objects.filter(uuid=pages_data[0].uuid).first()
    assert response.status_code == 200
    assert page.unblock_date.strftime("%d.%m.%Y %H:%M") == unblock_date


def test_block_page_user(api_client, pages_data):
    unblock_date = (datetime.utcnow() + timedelta(days=1)).strftime("%d.%m.%Y %H:%M")
    response = api_client.patch(f"{endpoint}{pages_data[0].uuid}/block-page/",
                                data={'unblock_date': unblock_date},
                                format="json")
    assert response.status_code == 403


def test_unblock_page(admin_api_client, blocked_page_data):
    response = admin_api_client.patch(f"{endpoint}{blocked_page_data.uuid}/unblock-page/")
    page = Page.objects.filter(uuid=blocked_page_data.uuid).first()
    assert response.status_code == 200
    assert page.unblock_date is None


def test_unblock_page_user(api_client, blocked_page_data):
    response = api_client.patch(f"{endpoint}{blocked_page_data.uuid}/unblock-page/")
    assert response.status_code == 403


def test_change_permanent_block_status(admin_api_client, pages_data):
    response = admin_api_client.patch(f"{endpoint}{pages_data[0].uuid}/change-permanent-block/")
    page = Page.objects.filter(uuid=pages_data[0].uuid).first()
    assert response.status_code == 200
    assert page.is_blocked_permanently


def test_change_permanent_block_status_user(api_client, pages_data):
    response = api_client.patch(f"{endpoint}{pages_data[0].uuid}/change-permanent-block/")
    assert response.status_code == 403
