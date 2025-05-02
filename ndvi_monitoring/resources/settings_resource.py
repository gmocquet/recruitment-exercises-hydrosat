from dagster import ConfigurableResource, EnvVar
from typing import get_type_hints, Optional, get_origin, get_args, Union
import os
from pathlib import Path


class SettingsResource(ConfigurableResource):
  aws_profile: Optional[str]
  aws_region: str = EnvVar("AWS_REGION")
  aws_s3_endpoint: str = EnvVar("AWS_S3_ENDPOINT")
  aws_s3_pipeline_bucket_name: str = EnvVar("AWS_S3_PIPELINE_BUCKET_NAME")
  aws_s3_use_ssl: bool = EnvVar("AWS_S3_USE_SSL")

  tmp_dir: str = EnvVar("TMP_DIR")
  stac_api_url: str = EnvVar("STAC_API_URL")

  @staticmethod
  def create():
    """
    Main usage, create a SettingsResource instance at the runtime (e.g. in a Dagster pipeline)
    """
    settings = SettingsResource()
    settings._post_init()
    return settings

  @staticmethod
  def create_from_env():
    """
    Use for testing, create a SettingsResource instance from environment variables
    due to EnvVar have a different behavior in test and runtime.
    """
    env_values = {}
    for attr_name, attr_type in get_type_hints(SettingsResource).items():
      env_var_name = attr_name.upper()
      env_values[attr_name] = os.environ.get(env_var_name)
    settings = SettingsResource(**env_values)
    settings._post_init()
    return settings

  def create_tmp_dir(self):
    tmp_dir = Path(self.tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

  def validate(self):
    missing_vars = []

    for attr_name, attr_type in get_type_hints(self.__class__).items():
      attr_value = getattr(self, attr_name, None)

      # Check if it's an EnvVar
      if isinstance(attr_value, EnvVar):
        # Ignore if the type is Optional[...] (i.e. Union[..., NoneType])
        origin = get_origin(attr_type)
        args = get_args(attr_type)
        is_optional = origin is Union and type(None) in args

        if is_optional:
          continue  # Skip the check for this field

        value = attr_value.get_value()
        if value is None:
          missing_vars.append(attr_value.env_var_name)

    if missing_vars:
      raise ValueError(f"Missing mandatory environment variables: {', '.join(missing_vars)}")

  def _post_init(self):
    self.create_tmp_dir()
    self.validate()
