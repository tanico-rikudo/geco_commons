import boto3
from boto3.dynamodb.conditions import Key
class Dynamo:
    def __init__(self,  db='dynamodb',table=None):
        self.dynamodb = boto3.resource(db)
        self.table    = self.dynamodb.Table(table)

    def insert(self, item):
        self.table.put_item(item)

    def query(self, query, fetch_limit=1, asc_sort=True):
        query_data = self.table.query(
            KeyConditionExpression = query,
            ScanIndexForward = asc_sort,
            Limit = fetch_limit
        )
        return query_data


    