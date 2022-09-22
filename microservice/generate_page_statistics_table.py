import boto3

from database import get_database

database = get_database()

table = database.create_table(
    TableName='PageStatistics',
    KeySchema=[
        {
            'AttributeName': 'uuid',
            'KeyType': 'HASH'
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'uuid',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }

)
