import os

import boto3

from Innotwitter.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_ENDPOINT_URL, AWS_BUCKET_NAME


def check_image_extension(image_file):
    _, file_extension = os.path.splitext(image_file.name)
    return file_extension in ('jpg', 'jpeg', 'png')


def upload_image(image_file, folder):
    if image_file is None:
        raise Exception("Page image is not provided")

    if check_image_extension(image_file):
        return Exception("Incorrect page image extension")

    cloud_name = os.path.join(folder, image_file.name)
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                    region_name=AWS_REGION)
    s3 = session.resource("s3", endpoint_url=AWS_ENDPOINT_URL)

    s3.Bucket(AWS_BUCKET_NAME).put_object(Key=cloud_name, Body=image_file)

    return os.path.join(AWS_ENDPOINT_URL, cloud_name)

