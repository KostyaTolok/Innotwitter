import os

import boto3
from dotenv import load_dotenv

load_dotenv()


def get_database():
    database = boto3.client('dynamodb', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                            region_name=os.getenv('AWS_REGION'), endpoint_url=os.getenv('AWS_ENDPOINT_URL'))

    return database
