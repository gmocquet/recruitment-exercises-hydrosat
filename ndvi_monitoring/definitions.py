from dagster import Definitions, load_assets_from_modules

from ndvi_monitoring import assets  # noqa: TID252
from ndvi_monitoring.sensors.s3_file_sensor import s3_new_file_sensor, fields_job
from ndvi_monitoring.resources.settings_resource import SettingsResource
from ndvi_monitoring.resources.minio_s3_resource import MinioS3Resource
from ndvi_monitoring.resources.stac_resource import STACResource

all_assets = load_assets_from_modules([assets])

settings = SettingsResource.create()
s3 = MinioS3Resource(settings=settings)

defs = Definitions(
  assets=all_assets,
  jobs=[fields_job],
  sensors=[s3_new_file_sensor],
  resources={
    "s3": s3,
    "stac": STACResource(settings=settings),
    "settings": settings,
  },
)
