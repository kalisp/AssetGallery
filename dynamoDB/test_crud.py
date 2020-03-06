import boto3
import json
import decimal
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Assets')

with open('sample.json', 'r') as pf:
    assets = json.load(pf, parse_float = decimal.Decimal)

    for asset in assets:
        table.put_item(
            Item={
                'id'  :  str(uuid.uuid1()),
                'name'  : asset['name'],
                'version'  :  asset['version'],
                'author'  : asset['author'],
                'tags'  : asset['tags'],
                'last_updated'  : asset['last_updated'],
                'path'  : asset['path'],
                'screenshot_path'  : asset['screenshot_path']
            }
        )


response = table.scan()
print(response)
