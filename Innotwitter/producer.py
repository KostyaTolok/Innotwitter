import json

import aio_pika
from django.conf import settings


async def publish_message(data):
    connection = await aio_pika.connect_robust(settings.MICROSERVICE_BROKER_URL)

    async with connection:
        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(data).encode()),
            routing_key=settings.MICROSERVICE_QUEUE_NAME
        )
