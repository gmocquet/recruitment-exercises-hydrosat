import boto3
from dagster import ConfigurableResource
from ndvi_monitoring.resources.settings_resource import SettingsResource


class MinioS3Resource(ConfigurableResource):
  settings: SettingsResource

  def create_client(self):
    """
    Create an S3 client using settings from SettingsResource.

    Returns:
        boto3.client: Configured S3 client

    Raises:
        ValueError: If required settings are missing
    """
    profile_name = self.settings.aws_profile
    region_name = self.settings.aws_region
    endpoint_url = self.settings.aws_s3_endpoint

    session = boto3.Session(profile_name=profile_name, region_name=region_name)
    return session.client("s3", endpoint_url=endpoint_url, use_ssl=self.settings.aws_s3_use_ssl)

  def get_client(self):
    return self.create_client()
