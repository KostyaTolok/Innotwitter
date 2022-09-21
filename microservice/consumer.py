import json
import logging
import os
import asyncio

import aio_pika
from dotenv import load_dotenv

from database import get_database
from repositories import PageStatisticsRepository
from utils import MessageTypes
from schemas import CreatePageStatistics, PageStatistics

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = get_database()
page_statistics_repository = PageStatisticsRepository(database)


async def consume_message():
    connection = await aio_pika.connect_robust(os.getenv("MICROSERVICE_BROKER_URL"), loop=asyncio.get_running_loop())

    channel = await connection.channel()

    await channel.set_qos(prefetch_count=10)

    queue = await channel.declare_queue(os.getenv("MICROSERVICE_QUEUE_NAME"))

    await queue.consume(process_message)


async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        try:
            message = json.loads(message.body.decode())
            logger.info(f"Message received: {message}")
            message_type = message.get('type')
            page_uuid = message.get('uuid')

            if not page_uuid:
                raise Exception("Error creating page statistics: page uuid not found")

            if message_type == MessageTypes.CREATE.name:
                page_statistics = CreatePageStatistics(uuid=page_uuid)

                response = page_statistics_repository.create(page_statistics)

                if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    logger.info("Page statistics created")
            elif message_type == MessageTypes.UPDATE.name:
                followers_count = message.get('followers_count')
                posts_count = message.get('posts_count')

                if followers_count is not None and posts_count is not None:
                    page_statistics = PageStatistics(uuid=page_uuid,
                                                     followers_count=followers_count,
                                                     posts_count=posts_count)
                    response = page_statistics_repository.update(page_statistics)
                elif followers_count is not None:
                    page_statistics = PageStatistics(uuid=page_uuid, followers_count=followers_count)
                    response = page_statistics_repository.update_followers_count(page_statistics)
                elif posts_count is not None:
                    page_statistics = PageStatistics(uuid=page_uuid, posts_count=posts_count)
                    response = page_statistics_repository.update_posts_count(page_statistics)
                else:
                    raise Exception("Page statistics was not provided")

                if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    logger.info("Page statistics updated")

            elif message_type == MessageTypes.DELETE.name:
                response = page_statistics_repository.delete(page_uuid)

                if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    logger.info("Page statistics deleted")
        except Exception as e:
            logger.error(e)
