#!/bin/bash -e

source regions.sh

for region in "${PYPY35_REGIONS[@]}"; do
  bucket_name="iopipe-layers-${region}"

  echo "Creating bucket ${bucket_name}..."

  aws s3 mb s3://$bucket_name --region $region
done