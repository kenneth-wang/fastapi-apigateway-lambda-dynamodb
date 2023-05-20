import os

import boto3

dynamodb_client = boto3.resource(
    "dynamodb",
    endpoint_url=os.environ["DYNAMODB_ENDPOINT"],
    region_name="ap-southeast-1",
)
