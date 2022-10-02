from functools import lru_cache
from django.conf import settings

import boto3


@lru_cache
def get_client(service):
    client = boto3.client(service, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION, endpoint_url=settings.AWS_ENDPOINT_URL)
    return client


def upload_image(image_file, image_key):
    client = get_client("s3")
    client.put_object(Bucket=settings.AWS_BUCKET_NAME, Key=image_key, Body=image_file)


def get_image_url(image_key):
    client = get_client("s3")
    return client.generate_presigned_url('get_object', Params={'Bucket': settings.AWS_BUCKET_NAME, 'Key': image_key})
