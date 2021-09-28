import re
import os
import time
import boto3
import uuid
from datetime import datetime
from botocore.client import Config
from .settings import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_STORAGE_BUCKET_NAME,REGION_NAME


ACCESS_KEY = AWS_ACCESS_KEY_ID
SECRET_KEY = AWS_SECRET_ACCESS_KEY
BUCKET_NAME = AWS_STORAGE_BUCKET_NAME

def get_ext(file):
    m = re.search(r'\.[A-Za-z0-9]+$', file)
    return m.group(0) if m else ""

# print(get_ext("hello.gif"))

def get_file_name(file):
    random_file_name = '-'.join([str(uuid.uuid4().hex[:14]), file])
    return random_file_name

    

# print(get_file_name("myapp_models.png"))

def upload(file, filetype, name):
    data = file
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    

    REGION = REGION_NAME
    today = datetime.now()
    # try:
    file_ext = get_ext(name)

    if file_ext == "":
        file_ext = 'png'
    filename = "ULTRAEXPERTS-{}-{}{}{}{}{}{}{}{}".format(filetype, today.year, today.month, today.day, today.hour, today.minute, today.second, today.microsecond, file_ext)
    filepath = '{}/{}/{}/{}/{}/{}'.format(filetype, today.year, today.month, today.day, today.hour, filename)
    s3.Bucket(BUCKET_NAME).put_object(Key=filepath, Body=data)
    object_acl = s3.ObjectAcl(BUCKET_NAME, filepath)
    response = object_acl.put(ACL='public-read')
    url = 'https://{}.s3.{}.amazonaws.com/{}/{}/{}/{}/{}/{}'.format(str(BUCKET_NAME), str(REGION), str(filetype), str(today.year), str(today.month), str(today.day), str(today.hour), str(filename))

    return url, file_ext
    