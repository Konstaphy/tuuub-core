import datetime
import os

import boto3
from botocore.client import BaseClient
from werkzeug.datastructures import FileStorage


class S3Exception(Exception):
    pass


class S3Service:
    s3client: BaseClient = None
    _bucket: str = "tuub"

    def __init__(self):
        self.s3client = boto3.client(
                                     service_name='s3',
                                     endpoint_url='https://storage.yandexcloud.net',
                                     aws_access_key_id=os.environ['S3_AWS_KEY_ID'],
                                     aws_secret_access_key=os.environ['S3_AWS_SECRET_KEY'])

    # get file from s3, proxy between front and s3 backend
    def get_file(self, key: str):
        try:
            return self.s3client.get_object(Bucket=self._bucket, Key=key)['Body'].read()
        except BaseException:
            raise S3Exception("Failed to get file")

    # uploading video to s3 with name depended on current time
    def upload_video(self, file: FileStorage):
        try:
            title = "videos/" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + file.filename
            title = title.replace(" ", "")
            self.s3client.upload_fileobj(file,
                                         self._bucket,
                                         title)
            return title
        except BaseException as e:
            print(e)
            raise S3Exception("Failed to upload video")
