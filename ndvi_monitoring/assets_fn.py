from typing import Generator
from dagster_aws.s3 import S3Resource
from ndvi_monitoring.resources.settings_resource import SettingsResource
from dagster import OpExecutionContext
import json
from jsonpath_ng.ext import parse
import rasterio
import numpy as np

from rasterio.windows import from_bounds
from shapely.geometry import shape


def move_s3_objects_between_prefixes(
  context: OpExecutionContext, s3: S3Resource, settings: SettingsResource, prefix_src: str, prefix_dest: str
) -> None:
  """
  Move all S3 objects from prefix_src to prefix_dest within the same bucket.
  """
  bucket_name = settings.aws_s3_pipeline_bucket_name
  s3_client = s3.create_client()

  paginator = s3_client.get_paginator("list_objects_v2")
  page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix_src)

  context.log.debug(f"Moving objects from {prefix_src} to {prefix_dest}")

  for page in page_iterator:
    for obj in page.get("Contents", []):
      source_key = obj["Key"]
      destination_key = source_key.replace(prefix_src, prefix_dest, 1)

      # Copy the object to the new location
      s3_client.copy_object(
        Bucket=bucket_name, CopySource={"Bucket": bucket_name, "Key": source_key}, Key=destination_key
      )

      # Delete the original object
      s3_client.delete_object(Bucket=bucket_name, Key=source_key)

      context.log.debug(f"Moved {source_key} to {destination_key}")


def read_band_window(url: str, bbox_geom: dict) -> np.ndarray:
  bbox = bbox_geom
  if isinstance(bbox_geom, dict):
    bbox = shape(bbox_geom)

  with rasterio.open(url) as src:
    window = from_bounds(*bbox.bounds, transform=src.transform)  # type: ignore
    data = src.read(1, window=window).astype("float32")
    return data


def compute_ndvi_from_cog_urls(red_url: str, nir_url: str, bbox_geom: dict | None = None) -> np.ndarray:
  with rasterio.open(red_url) as red_src, rasterio.open(nir_url) as nir_src:
    if bbox_geom:
      red = read_band_window(red_url, bbox_geom)
      nir = read_band_window(nir_url, bbox_geom)

    red = red_src.read(1).astype("float32")
    nir = nir_src.read(1).astype("float32")

  ndvi = (nir - red) / (nir + red + 1e-6)
  return ndvi


def yield_s3_files_staticdata_geojson(context, s3: S3Resource, settings: SettingsResource, S3_PREFIX: str) -> Generator:
  S3_BUCKET = settings.aws_s3_pipeline_bucket_name
  s3_client = s3.create_client()
  response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_PREFIX)
  if "Contents" not in response:
    context.log.warning(f"No files found in {S3_BUCKET}/{S3_PREFIX}")

  for obj in response.get("Contents", []):
    key = obj["Key"]
    if key.endswith(".geojson"):
      context.log.debug(f"Loading {key}")

      s3_object = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
      try:
        content = json.loads(s3_object["Body"].read().decode("utf-8"))
        context.log.debug(f"Yielding {key}")
        yield key, content
      except Exception as e:
        context.log.error(f"Error processing {key}: {e}")


def yield_fields_staticdata_geojson(context, s3_content) -> Generator:
  jsonpath_expr = parse('$.features[?(@.properties["object-type"] == "field")]')
  for match in jsonpath_expr.find(s3_content):
    yield str(match.value["properties"]["object-id"]), match.value
