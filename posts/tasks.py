import boto3
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

logger = get_task_logger(__name__)


@shared_task
def send_notification(emails, page_name):
    ses_client = boto3.client("ses", region_name=settings.AWS_REGION, endpoint_url=settings.AWS_ENDPOINT_URL)

    charset = 'UTF-8'
    try:
        response = ses_client.send_email(
            Destination={
                "ToAddresses": emails
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": charset,
                        "Data": f"New post from {page_name} arrived",
                    }
                },
                "Subject": {
                    "Charset": charset,
                    "Data": "New post notification",
                },
            },
            Source=settings.EMAIL_SENDER,
        )
        logger.info(response)
    except Exception as error:
        logger.error(error)
