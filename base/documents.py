import boto3

from django.conf import settings

from base.choices import CONTENT_TYPE

from base.exceptions import BaseAPIException


class DocumentUploadHandler:
    bucket_name = None
    client_s3 = None
    resource_s3 = None

    def __init__(self, bucket_name):
        self.client_s3 = boto3.client(
            's3',
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY
        )
        self.resource_s3 = boto3.resource(
            's3',
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY
        )
        self.bucket_name = bucket_name

    def upload_document(self, file_obj, key, preview_required=False):
        file_format = file_obj.name.split('.')[-1]
        ExtraArgs = {
            'ContentType': CONTENT_TYPE.get(file_format)
        }
        try:
            self.is_preview_available(
                file_format, preview_required)
            self.client_s3.upload_fileobj(
                file_obj.file,
                self.bucket_name,
                key,
                ExtraArgs=ExtraArgs
            )
        except Exception as e:
            print(e)
            try:
                self.client_s3.upload_file(
                    file_obj.name,
                    self.bucket_name,
                    key,
                    ExtraArgs=ExtraArgs
                )
            except Exception as e:
                print(e)
                raise BaseAPIException(
                    'Validation Failed', 'validation_failed'
                )
        return self.get_file_public_url(
            self.get_bucket_region(), key)

    def is_preview_available(self, file_format, preview_required):
        if preview_required and file_format not in CONTENT_TYPE.keys():
            raise BaseAPIException(
                'Incorrect file format',
                'incorrect_file_format'
            )

    def get_bucket_region(self):
        return self.client_s3.get_bucket_location(
            Bucket=self.bucket_name)['LocationConstraint']

    def get_file_public_url(self, bucket_location, key):
        return 'https://' + self.bucket_name + '.s3.' + bucket_location + '.amazonaws.com/' + key
