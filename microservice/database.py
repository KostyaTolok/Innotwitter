import os

import boto3
from configs import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_ENDPOINT_URL


def get_database():
    database = boto3.client('dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION, endpoint_url=AWS_ENDPOINT_URL)
    return database
