import boto3
import os

DEFAULT_BUCKET_NAME = os.environ.get("BUCKET_NAME")
PROFILE_NAME = os.environ.get("PROFILE_NAME")

class _FileProcessor:
    _instance = None

    def __init__(self, bucket=DEFAULT_BUCKET_NAME):
        session = boto3.Session(profile_name=PROFILE_NAME)
        self.s3_client = session.client('s3')
        self.s3_resource_session = session.resource('s3')
        self.bucket_name = bucket
        self.bucket = self.s3_resource_session.Bucket(bucket)

    def retrieve_file_names(self):
        return [
            obj.key for obj in self.bucket.objects.all()
        ]

    def upload_file(self, file_name, file_path):
        with open(file_path, 'rb') as f:
            self.bucket.upload_fileobj(f, file_name)

    def delete_file(self, file_name):
        # delete file from s3
        self.bucket.delete_objects(Delete={'Objects': [{'Key': file_name}]})

    def fetch_file_url(self, file_name):
        # get file url from s3
        return self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': file_name},
            ExpiresIn=60)

    def delete_all(self):
        self.bucket.objects.all().delete()


# enforce Singleton
def FileProcessor(*args, **kwargs):
    if _FileProcessor._instance is None:
        _FileProcessor._instance = _FileProcessor(*args, **kwargs)
    return _FileProcessor._instance
