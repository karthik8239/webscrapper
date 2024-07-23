import boto3
from botocore.exceptions import ClientError

def check_bucket_exists(bucket_name):
    """
    Check if an S3 bucket exists.
    :param bucket_name: Name of the bucket to check.
    :return: True if bucket exists, else False.
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False

def create_bucket(bucket_name):
    """
    Create an S3 bucket using boto3.
    :param bucket_name: Name of the bucket to create.
    :return: True if bucket was created, else False.
    """
    try:
        s3_client = boto3.client('s3')
        location = {'LocationConstraint': 'us-east-2'}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print(f"Error creating the bucket: {e}")
        return False
    return True

def upload_to_s3(file_name, bucket_name, object_name=None):
    """
    Upload a file to an S3 bucket.
    :param file_name: File to upload.
    :param bucket_name: Bucket to upload to.
    :param object_name: S3 object name. If not specified then file_name is used.
    :return: True if file was uploaded, else False.
    """
    if object_name is None:
        object_name = file_name
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
        print(response)
    except Exception as e:
        print(f"Error uploading the file: {str(e)}")
        return False
    return True
