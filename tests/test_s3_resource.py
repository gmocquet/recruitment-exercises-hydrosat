import pytest
from ndvi_monitoring.resources.minio_s3_resource import MinioS3Resource
from ndvi_monitoring.resources.settings_resource import SettingsResource
import uuid


@pytest.fixture(scope="module")
def settings():
  return SettingsResource.create_from_env()


@pytest.fixture(scope="module")
def s3_client(settings):
  s3_resource = MinioS3Resource(settings=settings)
  return s3_resource.create_client()


def test_minio_integration(s3_client):
  bucket_name = f"test-bucket-{uuid.uuid4()}"
  object_key = "test.txt"
  test_data = b"Fake data for test"

  s3_client.create_bucket(Bucket=bucket_name)
  s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=test_data)

  response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
  downloaded_data = response["Body"].read()

  assert downloaded_data == test_data

  s3_client.delete_object(Bucket=bucket_name, Key=object_key)
  s3_client.delete_bucket(Bucket=bucket_name)
