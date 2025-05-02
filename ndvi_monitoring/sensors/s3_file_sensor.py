from dagster import sensor, RunRequest, SkipReason, define_asset_job, DefaultSensorStatus
from dagster_aws.s3 import S3Resource
from ndvi_monitoring.resources.settings_resource import SettingsResource
import json

AWS_S3_PIPELINE_STATICDATA_FIELDS_PENDING_KEY = "staticdata/fields/pending"
AWS_S3_PIPELINE_STATICDATA_FIELDS_PROCESSED_KEY = "staticdata/fields/processed"

fields_job = define_asset_job(name="fields_job", selection=["fields"])


@sensor(job=fields_job, minimum_interval_seconds=5, default_status=DefaultSensorStatus.RUNNING)
def s3_new_file_sensor(
  context,
  s3: S3Resource,
  settings: SettingsResource,
):
  s3_client = s3.create_client()
  bucket = settings.aws_s3_pipeline_bucket_name
  prefix = AWS_S3_PIPELINE_STATICDATA_FIELDS_PENDING_KEY

  response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
  all_files = [obj["Key"] for obj in response.get("Contents", [])]

  previous_files = json.loads(context.cursor) if context.cursor else []

  new_files = list(set(all_files) - set(previous_files))

  if new_files:
    # Update the cursor with the current list of files
    context.update_cursor(json.dumps(all_files))
    for file_key in new_files:
      yield RunRequest(run_key=file_key)
  else:
    context.update_cursor(json.dumps(all_files))
    yield SkipReason("No new files found")
