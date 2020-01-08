import boto3
from decouple import config

def get_s3():
    client = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'), aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
    s3 = boto3.resource('s3')
    return client