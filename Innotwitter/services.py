import os

import boto3

from django.conf import settings


def upload_image(image_file, folder):
    cloud_name = os.path.join(folder, image_file.name)
    client = boto3.client("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION, endpoint_url=settings.AWS_ENDPOINT_URL)

    client.put_object(Bucket=settings.AWS_BUCKET_NAME, Key=cloud_name, Body=image_file)

    return os.path.join(settings.AWS_ENDPOINT_URL, cloud_name)
