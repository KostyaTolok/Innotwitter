import os
from dotenv import load_dotenv

load_dotenv()

MICROSERVICE_BROKER_URL = os.getenv("MICROSERVICE_BROKER_URL")
MICROSERVICE_QUEUE_NAME = os.getenv("MICROSERVICE_QUEUE_NAME")

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL')