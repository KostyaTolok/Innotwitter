from exceptions import NotFoundException


class PageStatisticsRepository:
    def __init__(self, db):
        self.table_name = "PageStatistics"
        self.__db = db

    def list(self):
        response = self.__db.scan(TableName=self.table_name)
        return response.get('Items', [])

    def retrieve(self, page_uuid):
        response = self.__db.get_item(TableName=self.table_name, Key={'uuid': {'S': page_uuid}})
        item = response.get('Item')
        if not item:
            raise NotFoundException("Page statistics not found")
        return item

    def create(self, statistics):
        response = self.__db.put_item(TableName=self.table_name, Item={
            "uuid": {"S": statistics.uuid},
            "owner_username": {"S": statistics.owner_username}
        })
        return response

    def update(self, statistics):
        response = self.__db.update_item(
            TableName=self.table_name,
            Key={
                'uuid': {'S': statistics.uuid}
            },
            UpdateExpression=
            """                
                set followers_count=:followers_count, posts_count=:posts_count
            """,
            ExpressionAttributeValues={
                ':followers_count': {'N': str(statistics.followers_count)},
                ':posts_count': {'N': str(statistics.posts_count)},
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def update_followers_count(self, statistics):
        response = self.__db.update_item(
            TableName=self.table_name,
            Key={
                'uuid': {'S': statistics.uuid}
            },
            UpdateExpression=
            """                
                set followers_count=:followers_count
            """,
            ExpressionAttributeValues={
                ':followers_count': {'N': str(statistics.followers_count)},
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def update_posts_count(self, statistics):
        response = self.__db.update_item(
            TableName=self.table_name,
            Key={
                'uuid': {'S': statistics.uuid}
            },
            UpdateExpression=
            """                
                set posts_count=:posts_count
            """,
            ExpressionAttributeValues={
                ':posts_count': {'N': str(statistics.posts_count)},
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete(self, page_uuid):
        response = self.__db.delete_item(
            TableName=self.table_name,
            Key={
                'uuid': {'S': page_uuid}
            }
        )
        return response
