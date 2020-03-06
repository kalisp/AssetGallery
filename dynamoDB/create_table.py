import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="http://localhost:8000")

# table = dynamodb.Table('Assets')
# print(table)
# if table:
#     table.delete()
# # print(table)

table = dynamodb.create_table(
    TableName = 'Users',
    KeySchema = [
        {
            "AttributeName" : 'user_name',
            "KeyType"       : 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName' : 'user_name',
            'AttributeType' : 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

# table = dynamodb.create_table(
#     TableName = 'Assets',
#     KeySchema = [
#         {
#             'AttributeName' : 'id',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName' : 'name',
#             'KeyType': 'RANGE'
#         },
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName' : 'id',
#             'AttributeType' : 'S'
#         },
#         {
#             'AttributeName' : 'name',
#             'AttributeType' : 'S'
#         },
#         # {
#         #     'AttributeName' : 'author',
#         #     'AttributeType' : 'S'
#         # },
#         # {
#         #     'AttributeName' : 'date_created',
#         #     'AttributeType' : 'S'
#         # },
#         # {
#         #     'AttributeName': 'version',
#         #     'AttributeType': 'N'
#         # },
#         # {
#         #     'AttributeName': 's3_path',
#         #     'AttributeType': 'S'
#         # },
#         # {
#         #     'AttributeName': 'screenshot_path',
#         #     'AttributeType': 'S'
#         # },
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 10,
#         'WriteCapacityUnits': 10
#     }
#
# )
#
# print("Table {}".format(table.table_status))