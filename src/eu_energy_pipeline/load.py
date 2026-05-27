from eu_energy_pipeline.exceptions import LoadError
from eu_energy_pipeline.logger import get_logger
import boto3
from datetime import datetime, timezone
import json


class S3Loader:
    def __init__(
        self,
        aws_access_key_id,
        aws_secret_access_key,
        aws_region,
        prefix,
        aws_bucket_name,
    ):

        self.logger = get_logger(__name__)
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

        self.prefix = prefix
        self.bucket_name = aws_bucket_name

    def s3_uploader(self, data, endpoint, ingestion_date):
        try:
            self.logger.info(f"Initiating data upload to S3 bucket: {self.bucket_name}")

            today = datetime.now(timezone.utc)
            year = today.strftime("%Y")
            month = today.strftime("%m")
            day = today.strftime("%d")
            timestamp = today.strftime("%H%M%S")

            payload = {
                "ingestion_date": ingestion_date,
                "endpoint": endpoint,
                "data": data,
                "year": year,
                "month": month,
                "day": day,
                "timestamp": timestamp,
            }

            s3_key = (
                f"{self.prefix}/"
                f"endpoint={endpoint}/"
                f"year={year}/"
                f"month={month}/"
                f"day={day}/"
                f"agsi_{endpoint}_{timestamp}.json"
            )
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json.dumps(payload),
                ContentType="application/json",
            )
            self.logger.info(f"Successfully uploaded data to S3 with key: {s3_key}")
            return s3_key
        except Exception as e:
            raise LoadError(f"Failed to upload data to S3: {str(e)}")
