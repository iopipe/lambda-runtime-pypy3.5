#!/bin/bash -e

source regions.sh

MD5SUM=$(md5 -q pypy35.zip)
S3KEY="pypy3.5/${MD5SUM}"

for region in "${PYPY35_REGIONS[@]}"; do
  bucket_name="iopipe-layers-${region}"

  echo "Uploading pypy35.zip to s3://${bucket_name}/${S3KEY}"

  aws --region $region s3 cp pypy35.zip "s3://${bucket_name}/${S3KEY}"
done
