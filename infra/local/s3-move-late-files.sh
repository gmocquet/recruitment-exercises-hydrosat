#!/usr/bin/env bash
set -eu

# Get the directory where the script is located
# Use realpath to get the absolute path
SCRIPT_ROOT_DIR="$(realpath $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"

aws s3 mv \
    s3://${AWS_S3_PIPELINE_BUCKET_NAME}/staticdata/late-fields/ \
    s3://${AWS_S3_PIPELINE_BUCKET_NAME}/staticdata/fields/pending/ \
    --recursive \
    --exclude "*" \
    --include "*.geojson" \
    --profile ${AWS_PROFILE} \
    --endpoint-url ${AWS_S3_ENDPOINT}
