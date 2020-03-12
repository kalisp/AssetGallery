Flask library app:
===============
Build on: Flask, DynamoDB, WTForms, requests, boto3
Author: petr.kalis@gmail.com, 2020

Server part of Maya ControllerLibrary. Allows storing metadata about controllers in DynamoDB,
stores screenshot and controller files (maya .ma) in S3 bucket.

Allows listing of stored assets, allows searching by tags, allows basic authentication.

Future development: edit assets, user roles and permissions, search asset by name