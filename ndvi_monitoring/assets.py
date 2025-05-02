from dagster import (
  asset,
  AssetDep,
  AssetSpec,
  DailyPartitionsDefinition,
  MultiPartitionsDefinition,
  DimensionPartitionMapping,
  DynamicPartitionsDefinition,
  MultiPartitionMapping,
  TimeWindowPartitionMapping,
  Output,
  Definitions,
  AutoMaterializePolicy,
)
from ndvi_monitoring.domain.bbox import Bbox
from ndvi_monitoring.domain.field import Field, NDVI
from typing import List
import geopandas as gpd
import io
from ndvi_monitoring.sensors.s3_file_sensor import (
  AWS_S3_PIPELINE_STATICDATA_FIELDS_PENDING_KEY,
  AWS_S3_PIPELINE_STATICDATA_FIELDS_PROCESSED_KEY,
)
from dagster_aws.s3 import S3Resource
from ndvi_monitoring.resources.settings_resource import SettingsResource
from ndvi_monitoring.resources.stac_resource import STACResource
from ndvi_monitoring.resources.minio_s3_resource import MinioS3Resource
from shapely.geometry import mapping, shape

from ndvi_monitoring.assets_fn import (
  yield_s3_files_staticdata_geojson,
  yield_fields_staticdata_geojson,
  compute_ndvi_from_cog_urls,
  move_s3_objects_between_prefixes,
)

daily_partitions = DailyPartitionsDefinition(start_date="2025-04-01")

field_partitions = DynamicPartitionsDefinition(name="field_id")

multi_partitions = MultiPartitionsDefinition(
  {
    "date": daily_partitions,
    "field_id": field_partitions,
  }
)


@asset
def bbox(s3: S3Resource, settings: SettingsResource) -> Bbox:
  """
  Load the bbox from the s3 bucket staticdata prefix.
  """
  s3_client = s3.create_client()
  response = s3_client.get_object(Bucket=settings.aws_s3_pipeline_bucket_name, Key="staticdata/config/bbox.geojson")
  content = response["Body"].read()
  bbox = gpd.read_file(io.BytesIO(content))
  return Bbox.from_geodataframe(bbox)


@asset
def fields(context, s3: S3Resource, settings: SettingsResource) -> List[Field]:
  """
  Load all fields from s3 bucket staticdata prefix.
  """
  field_ids = set()
  fields = []

  for _, s3_content in yield_s3_files_staticdata_geojson(
    context, s3, settings, AWS_S3_PIPELINE_STATICDATA_FIELDS_PENDING_KEY
  ):
    for field_id, field in yield_fields_staticdata_geojson(context, s3_content):
      field_obj = Field(
        id=field_id,
        plant_type=field["properties"]["plant-type"],
        plant_date=field["properties"]["plant-date"],
        geom=field["geometry"],
      )
      fields.append(field_obj)
      field_ids.add(field_id)

  if not field_ids:
    context.log.warning("No field found")
    return []

  move_s3_objects_between_prefixes(
    context,
    s3,
    settings,
    AWS_S3_PIPELINE_STATICDATA_FIELDS_PENDING_KEY,
    AWS_S3_PIPELINE_STATICDATA_FIELDS_PROCESSED_KEY,
  )

  instance = context.instance
  instance.add_dynamic_partitions(partitions_def_name="field_id", partition_keys=list(field_ids))
  context.log.info(f"✅ Added {len(field_ids)} dynamic partitions for field_id.")

  return fields


@asset(
  partitions_def=multi_partitions,
  auto_materialize_policy=AutoMaterializePolicy.eager(),
  deps=[
    fields,
    bbox,
    AssetDep(  # asset depend on the previous day's data (compute all field_id partitions for a given day)
      AssetSpec("field_ndvi"),  # upstream asset
      partition_mapping=MultiPartitionMapping(
        {
          "date": DimensionPartitionMapping(
            dimension_name="date",
            partition_mapping=TimeWindowPartitionMapping(start_offset=-1, end_offset=-1),
          ),
        }
      ),
    ),
  ],
)
def field_ndvi(context, stac: STACResource, bbox: Bbox, fields: List[Field]) -> Output[Field]:
  """
  Compute the NDVI for a given field at a given date.
  """
  date_str = context.partition_key.keys_by_dimension["date"]
  field_id = context.partition_key.keys_by_dimension["field_id"]
  field = next((f for f in fields if f.id == field_id), None)

  if field is None:
    raise ValueError(f"Field {field_id} not found")

  if date_str < field.plant_date:
    context.log.info(f"Field {field_id} not planted yet on {date_str}. Skipping NDVI computation.")
    return Output(
      field,
      metadata={
        "success": False,
        "error": f"Field {field_id} not planted yet on {date_str}",
        "ndvi_computed": False,
      },
    )

  context.log.info(f"Compute NDVI for field {field_id} (plant_date: {field.plant_date}, plant_type: {field.plant_type}) on date {date_str}")

  field_in_bbox = mapping(shape(field.geom).intersection(shape(bbox.geom)))

  stac_client = stac.create_client()

  items = stac_client.search(
    collections=["sentinel-2-l2a"],
    intersects=field_in_bbox,
    datetime=f"{date_str}/{date_str}",
    query={"eo:cloud_cover": {"lt": 30}},
  ).items()

  items = list(items)

  if len(items) == 0:
    context.log.info(f"No items found for {date_str}")
    return Output(
      field,
      metadata={
        "success": False,
        "error": f"No Sentinel-2 items found for {date_str}",
        "ndvi_computed": False,
      },
    )

  # Assuming taking the first item
  item = items[0]

  ndvi = compute_ndvi_from_cog_urls(
    red_url=item.assets["red"].href,
    nir_url=item.assets["nir"].href,
    bbox_geom=field_in_bbox,
  )

  context.log.info(f"✅ NDVI for {field_id} on {date_str} computed.")

  return Output(
    field.model_copy(update={"ndvi": NDVI.from_array(ndvi)}),
    metadata={
      "success": True,
      "error": None,
      "ndvi_computed": True,
    },
  )


settings = SettingsResource.create()
s3 = MinioS3Resource(settings=settings)


defs = Definitions(
  assets=[bbox, fields, field_ndvi],
  resources={
    "s3": s3,
    "stac": STACResource(settings=settings),
    "settings": settings,
  },
)
