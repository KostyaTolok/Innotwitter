import logging

import jwt

from database import get_database
from exceptions import ValidationException
from schemas import PageStatistics, CreatePageStatistics
from repositories import PageStatisticsRepository
from configs import JWT_SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = get_database()
page_statistics_repository = PageStatisticsRepository(database)


def create_page_statistics(page_uuid, owner_username):
    page_statistics = CreatePageStatistics(uuid=page_uuid, owner_username=owner_username)
    page_statistics_repository.create(page_statistics)
    logger.info("Page statistics created")


def update_page_statistics(page_uuid, followers_count, posts_count):
    if followers_count is not None and posts_count is not None:
        page_statistics = PageStatistics(uuid=page_uuid,
                                         followers_count=followers_count,
                                         posts_count=posts_count)
        page_statistics_repository.update(page_statistics)
    elif followers_count is not None:
        page_statistics = PageStatistics(uuid=page_uuid, followers_count=followers_count)
        page_statistics_repository.update_followers_count(page_statistics)
    elif posts_count is not None:
        page_statistics = PageStatistics(uuid=page_uuid, posts_count=posts_count)
        page_statistics_repository.update_posts_count(page_statistics)
    else:
        raise Exception("Page statistics was not provided")

    logger.info("Page statistics updated")


def delete_page_statistics(page_uuid):
    page_statistics = PageStatistics(uuid=page_uuid)
    page_statistics_repository.delete(page_statistics.uuid)
    logger.info("Page statistics deleted")


def retrieve_page_statistics(page_uuid):
    page_statistics_data = page_statistics_repository.retrieve(page_uuid)
    page_statistics = PageStatistics(uuid=page_statistics_data['uuid']['S'])
    followers_count = page_statistics_data.get('followers_count')
    posts_count = page_statistics_data.get('posts_count')
    owner_username = page_statistics_data.get('owner_username')

    if followers_count:
        page_statistics.followers_count = followers_count.get('N')

    if posts_count:
        page_statistics.posts_count = posts_count.get('N')

    if owner_username:
        page_statistics.owner_username = owner_username.get('S')

    return page_statistics


def validate_page_owner(token, page_owner_username):
    if not token:
        raise ValidationException("Authentication credentials were not provided")

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValidationException("Authentication token has expired")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise ValidationException("Authorization has failed, token is invalid")

    username = payload.get("username", None)

    if not username:
        raise ValidationException("Username was not provided")

    if username != page_owner_username:
        raise ValidationException("User is not page owner")
