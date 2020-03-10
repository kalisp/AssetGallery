import boto3
from dynamoDB import create_table
from config import Config
from flask import Flask

# for deleting tables on Win localhost
import os
from dateutil import tz
import time

if os.name == 'nt':
    def _naive_is_dst(self, dt):
        timestamp = tz.tz._datetime_to_timestamp(dt)
        # workaround the bug of negative offset UTC prob
        if timestamp+time.timezone < 0:
            current_time = timestamp + time.timezone + 31536000
        else:
            current_time = timestamp + time.timezone
        return time.localtime(current_time).tm_isdst

tz.tzlocal._naive_is_dst = _naive_is_dst

app = Flask(__name__)
app.config.from_object(Config)

dynamodb = boto3.resource('dynamodb', region_name=app.config['AWS_REGION'], endpoint_url=app.config['DYNAMODB_ENDPOINT'])

tables = ['Assets', 'Users']
for table_name in tables:
    table = dynamodb.Table(table_name)
    print('Deleting {} table'.format(table_name))
    table.delete()

print('Recreating Assets table')
create_table.create_asset_table(dynamodb)
print('Recreating User table')
create_table.create_user_table(dynamodb)

s3 = boto3.resource('s3')
bucket = s3.Bucket(app.config['FLASKS3_BUCKET_NAME'])
print('Deleting screenshots folder')
bucket.objects.filter(Prefix="screenshots/").delete()
print('Deleting assets folder')
bucket.objects.filter(Prefix="assets/").delete()