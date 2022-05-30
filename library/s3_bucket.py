import boto3
import os
from dotenv import load_dotenv
load_dotenv()


def s3_instance():
    s3 = boto3.resource(
        service_name='s3',
        region_name=os.environ['REGION'],
        aws_access_key_id=os.environ['ACCESS_KEY'],
        aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
    )
    return s3.Bucket(os.environ['BUCKET'])


def check_buckets():
    s3 = s3_instance()
    print(f'Bucket Creation Date: {s3.creation_date}')
    if len(list(s3.objects.all())) > 0:
        for object in s3.objects.all():
            print(f'Bucket contains: {object}')
    else:
        print('Bucket has no objects inside!')


def upload_file_to_s3(file_path):
    s3 = s3_instance()
    s3.upload_file(
        Filename=file_path,
        Key=os.path.basename(file_path),
    )
    print('File uploaded to S3 successfully!')


def delete_file_from_s3(file_path):
    s3 = s3_instance()
    s3.delete_objects(
        Delete={
            'Objects': [
                {
                    'Key': os.path.basename(file_path)
                }
            ]
        }
    )
    print('File deleted successfully!')


if __name__ == '__main__':
    check_buckets()
