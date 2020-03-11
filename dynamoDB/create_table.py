import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="http://localhost:8000")


def create_user_table(dynamodb):
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                "AttributeName": 'user_name',
                "KeyType": 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

def create_asset_table(dynamodb):
    table = dynamodb.create_table(
        TableName = 'Assets',
        KeySchema = [
            {
                'AttributeName' : 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName' : 'name',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName' : 'id',
                'AttributeType' : 'S'
            },
            {
                'AttributeName' : 'name',
                'AttributeType' : 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }

    )
