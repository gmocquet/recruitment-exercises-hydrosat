from dagster import ConfigurableResource
from ndvi_monitoring.resources.settings_resource import SettingsResource
from pystac_client import Client


class STACResource(ConfigurableResource):
  settings: SettingsResource

  def create_client(self):
    """
    Create an S3 client using settings from SettingsResource.

    Returns:
        boto3.client: Configured S3 client

    Raises:
        ValueError: If required settings are missing
    """

    stac_client = Client.open(self.settings.stac_api_url)

    return stac_client
