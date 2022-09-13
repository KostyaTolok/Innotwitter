import boto3
from celery import shared_task
from celery.utils.log import get_task_logger
from Innotwitter.settings import EMAIL_HOST, AWS_REGION, AWS_ENDPOINT_URL

logger = get_task_logger(__name__)


@shared_task
def send_notification(emails, page_name):
    ses_client = boto3.client("ses", region_name=AWS_REGION, endpoint_url=AWS_ENDPOINT_URL)
    response = ses_client.verify_email_identity(EmailAddress=EMAIL_HOST)
    logger.info(response)
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]

    if status_code == 200:
        charset = 'UTF-8'
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
            Source=EMAIL_HOST,
        )
        logger.info(response)