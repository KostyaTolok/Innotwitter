import json
from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status

from pages.models import Page


def test_list_200(api_client, pages_data):
    response = api_client.get(reverse("pages:pages-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(json.loads(response.content)) == 2


def test_retrieve_200(api_client, pages_data):
    response = api_client.get(reverse("pages:pages-detail", args=[pages_data[0].uuid]))
    page = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert page.get("name") == pages_data[0].name


def test_retrieve_blocked_403(api_client, blocked_page_data):
    response = api_client.get(reverse("pages:pages-detail", args=[blocked_page_data.uuid]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_retrieve_blocked_admin_200(admin_api_client, blocked_page_data):
    response = admin_api_client.get(reverse("pages:pages-detail", args=[blocked_page_data.uuid]))
    page = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert page.get("name") == blocked_page_data.name


def test_retrieve_private_403(second_api_client, private_page_data, second_user_data):
    response = second_api_client.get(reverse("pages:pages-detail", args=[private_page_data.uuid]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_retrieve_private_owner_200(api_client, private_page_data):
    response = api_client.get(reverse("pages:pages-detail", args=[private_page_data.uuid]))
    page = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert page.get("name") == private_page_data.name


def test_retrieve_private_admin_200(admin_api_client, private_page_data):
    response = admin_api_client.get(reverse("pages:pages-detail", args=[private_page_data.uuid]))
    page = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert page.get("name") == private_page_data.name


def test_create_201(api_client, pages_data):
    new_page_info = {"name": "New page",
                     "image_path": "http://127.0.0.1:8000/image",
                     "tags": [1]}
    response = api_client.post(reverse("pages:pages-list"), data=new_page_info, format="json")
    page = json.loads(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert page.get("name") == new_page_info.get("name")


def test_update_200(api_client, pages_data):
    response = api_client.put(reverse("pages:pages-detail", args=[pages_data[0].uuid]),
                              data={"name": "Updated page", "tags": [1]},
                              format="json")
    page = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert page.get("name") == "Updated page"


def test_update_not_owner_403(api_client, pages_data):
    response = api_client.put(reverse("pages:pages-detail", args=[pages_data[1].uuid]),
                              data={"name": "Updated page", "tags": [1]}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_destroy_204(api_client, pages_data):
    response = api_client.delete(reverse("pages:pages-detail", args=[pages_data[0].uuid]))
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_destroy_not_owner_403(api_client, pages_data):
    response = api_client.delete(reverse("pages:pages-detail", args=[pages_data[1].uuid]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_follow_200(api_client, pages_data, user_data):
    response = api_client.post(reverse("pages:pages-follow", args=[pages_data[1].uuid]))
    assert response.status_code == status.HTTP_200_OK
    assert pages_data[1].followers.contains(user_data)


def test_follow_private_200(api_client, pages_data, user_data):
    pages_data[1].is_private = True
    pages_data[1].save()
    response = api_client.post(reverse("pages:pages-follow", args=[pages_data[1].uuid]))
    assert response.status_code == status.HTTP_200_OK
    assert pages_data[1].follow_requests.contains(user_data)


def test_follow_owner_403(api_client, pages_data):
    response = api_client.post(reverse("pages:pages-follow", args=[pages_data[0].uuid]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_follow_already_follows_400(api_client, pages_data, user_data):
    pages_data[1].followers.add(user_data)
    response = api_client.post(reverse("pages:pages-follow", args=[pages_data[1].uuid]))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "User already follows this page"


def test_follow_already_sent_request_400(api_client, pages_data, user_data):
    pages_data[1].follow_requests.add(user_data)
    response = api_client.post(reverse("pages:pages-follow", args=[pages_data[1].uuid]))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "User already sent follow request to this page"


def test_unfollow_200(api_client, pages_data, user_data):
    pages_data[1].followers.add(user_data)
    response = api_client.post(reverse("pages:pages-unfollow", args=[pages_data[1].uuid]))
    assert response.status_code == status.HTTP_200_OK
    assert not pages_data[1].followers.contains(user_data)


def test_unfollow_doesnt_follow_400(api_client, pages_data, user_data):
    response = api_client.post(reverse("pages:pages-unfollow", args=[pages_data[1].uuid]))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "User doesn't follow this page"


def test_get_follow_requests_200(api_client, pages_data):
    response = api_client.get(reverse("pages:pages-get_follow_requests", args=[pages_data[0].uuid]))
    assert response.status_code == status.HTTP_200_OK
    assert len(json.loads(response.content)) == 1


def test_accept_follow_request_200(api_client, pages_data, admin_data):
    response = api_client.post(reverse("pages:pages-accept_follow_request", args=[pages_data[0].uuid]),
                               data={"user_id": 2}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert pages_data[0].followers.contains(admin_data)


def test_accept_follow_request_user_blocked_400(api_client, pages_data, admin_data):
    admin_data.is_blocked = True
    admin_data.save()
    response = api_client.post(reverse("pages:pages-accept_follow_request", args=[pages_data[0].uuid]),
                               data={"user_id": 2}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "User is blocked"


def test_accept_follow_request_no_follow_request_400(api_client, pages_data, admin_data):
    pages_data[0].follow_requests.remove(admin_data)
    response = api_client.post(reverse("pages:pages-accept_follow_request", args=[pages_data[0].uuid]),
                               data={"user_id": 2}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "User didn't send follow request"


def test_accept_follow_request_no_user_id_400(api_client, pages_data, admin_data):
    response = api_client.post(reverse("pages:pages-accept_follow_request", args=[pages_data[0].uuid]), format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_accept_all_follow_requests_200(api_client, pages_data, admin_data):
    response = api_client.post(reverse("pages:pages-accept_all_follow_requests", args=[pages_data[0].uuid]))
    assert response.status_code == status.HTTP_200_OK
    assert pages_data[0].followers.contains(admin_data)


def test_block_page_200(admin_api_client, pages_data):
    unblock_date = (datetime.utcnow() + timedelta(days=1)).strftime("%d.%m.%Y %H:%M")
    response = admin_api_client.patch(reverse("pages:pages-block_page", args=[pages_data[0].uuid]),
                                      data={'unblock_date': unblock_date},
                                      format="json")
    page = Page.objects.filter(uuid=pages_data[0].uuid).first()
    assert response.status_code == status.HTTP_200_OK
    assert page.unblock_date.strftime("%d.%m.%Y %H:%M") == unblock_date


def test_block_page_user_403(api_client, pages_data):
    unblock_date = (datetime.utcnow() + timedelta(days=1)).strftime("%d.%m.%Y %H:%M")
    response = api_client.patch(reverse("pages:pages-block_page", args=[pages_data[0].uuid]),
                                data={'unblock_date': unblock_date},
                                format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unblock_page_200(admin_api_client, blocked_page_data):
    response = admin_api_client.patch(reverse("pages:pages-unblock_page", args=[blocked_page_data.uuid]))
    page = Page.objects.filter(uuid=blocked_page_data.uuid).first()
    assert response.status_code == status.HTTP_200_OK
    assert page.unblock_date is None


def test_unblock_page_user_403(api_client, blocked_page_data):
    response = api_client.patch(reverse("pages:pages-unblock_page", args=[blocked_page_data.uuid]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_change_permanent_block_status_200(admin_api_client, pages_data):
    response = admin_api_client.patch(reverse("pages:pages-change_permanent_block_status", args=[pages_data[0].uuid]))
    page = Page.objects.filter(uuid=pages_data[0].uuid).first()
    assert response.status_code == status.HTTP_200_OK
    assert page.is_blocked_permanently


def test_change_permanent_block_status_user_403(api_client, pages_data):
    response = api_client.patch(reverse("pages:pages-change_permanent_block_status", args=[pages_data[0].uuid]))
    assert response.status_code == status.HTTP_403_FORBIDDEN
