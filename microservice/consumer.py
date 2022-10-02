import asyncio
import json
import logging

import aio_pika

from configs import MICROSERVICE_BROKER_URL, MICROSERVICE_QUEUE_NAME
from services import create_page_statistics, update_page_statistics, delete_page_statistics
from utils import MessageTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def consume_message():
    connection = await aio_pika.connect_robust(MICROSERVICE_BROKER_URL, loop=asyncio.get_running_loop())
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await channel.declare_queue(MICROSERVICE_QUEUE_NAME)
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
                owner_name = message.get("owner_username")

                if not owner_name:
                    raise Exception("Error creating page statistics: page owner not found")

                create_page_statistics(page_uuid, owner_name)
            elif message_type == MessageTypes.UPDATE.name:
                followers_count = message.get('followers_count')
                posts_count = message.get('posts_count')
                update_page_statistics(page_uuid, followers_count, posts_count)
            elif message_type == MessageTypes.DELETE.name:
                delete_page_statistics(page_uuid)
        except Exception as e:
            logger.error(e)
