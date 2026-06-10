import json
import pytest
from datetime import datetime, timezone

from eu_energy_pipeline.load import S3Loader
from eu_energy_pipeline.exceptions import LoadError


def test_s3_uploader_success(mocker):
    # Arrange

    fake_s3_client = mocker.Mock()

    mock_boto_client = mocker.patch(
        "eu_energy_pipeline.load.boto3.client",
        return_value=fake_s3_client
    )

    fixed_datetime = datetime(
        2026, 6, 10, 12, 34, 56, tzinfo=timezone.utc
    )

    mock_datetime = mocker.patch("eu_energy_pipeline.load.datetime")
    mock_datetime.now.return_value = fixed_datetime

    loader = S3Loader(
        aws_access_key_id="fake_access_key",
        aws_secret_access_key="fake_secret_key",
        aws_region="eu-central-1",
        prefix="raw",
        aws_bucket_name="eu-energy-bucket",
    )

    data = {
        "records": [
            {
                "facility": "test_facility",
                "value": 100
            }
        ]
    }

    endpoint = "storage"
    ingestion_date = "2026-06-10"

    # Act

    result = loader.s3_uploader(
        data=data,
        endpoint=endpoint,
        ingestion_date=ingestion_date
    )

    # Assert

    expected_key = (
        "raw/"
        "endpoint=storage/"
        "year=2026/"
        "month=06/"
        "day=10/"
        "agsi_storage_123456.json"
    )

    expected_payload = {
        "ingestion_date": "2026-06-10",
        "endpoint": "storage",
        "data": data,
        "year": "2026",
        "month": "06",
        "day": "10",
        "timestamp": "123456",
    }

    assert result == expected_key

    mock_boto_client.assert_called_once_with(
        "s3",
        aws_access_key_id="fake_access_key",
        aws_secret_access_key="fake_secret_key",
        region_name="eu-central-1",
    )

    fake_s3_client.put_object.assert_called_once_with(
        Bucket="eu-energy-bucket",
        Key=expected_key,
        Body=json.dumps(expected_payload),
        ContentType="application/json",
    )