import pytest
import os
from ndvi_monitoring.resources.settings_resource import SettingsResource


@pytest.fixture(scope="module")
def settings():
  return SettingsResource.create_from_env()


def str_to_bool(value: str) -> bool:
  return value.strip().lower() in ("true", "1", "yes", "y", "on")


def test_minio_integration(settings):
  assert settings.aws_profile == os.environ.get("AWS_PROFILE")
  assert settings.aws_region == os.environ.get("AWS_REGION")
  assert settings.aws_s3_endpoint == os.environ.get("AWS_S3_ENDPOINT")
  assert settings.aws_s3_pipeline_bucket_name == os.environ.get("AWS_S3_PIPELINE_BUCKET_NAME")
  assert settings.aws_s3_use_ssl == str_to_bool(os.environ.get("AWS_S3_USE_SSL"))
