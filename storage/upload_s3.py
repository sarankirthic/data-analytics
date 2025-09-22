import boto3
from config import Config
from processing.process_news import get_latest_raw_directory


def upload_to_s3(file_name, bucket_name, object_name=None):
    s3 = boto3.client('s3')
    if object_name is None:
        object_name = file_name
    s3.upload_file(file_name, bucket_name, object_name)


if __name__ == "__main__":
    processed_directory = Config.BASE_DIR / "data" / "processed" / get_latest_raw_directory(Config.BASE_DIR)
    upload_to_s3("processed_news.csv", Config.AWS_S3_BUCKET_NAME)
