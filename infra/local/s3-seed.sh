#!/usr/bin/env bash
set -eu

# Get the directory where the script is located
# Use realpath to get the absolute path
SCRIPT_ROOT_DIR="$(realpath $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"
DATA_DIR="$(realpath ${SCRIPT_ROOT_DIR}/../../seeding/s3)"

aws \
    --profile ${AWS_PROFILE} \
    --endpoint-url ${AWS_S3_ENDPOINT} \
    s3 sync \
    ${DATA_DIR}/ \
    s3://${AWS_S3_PIPELINE_BUCKET_NAME}/
