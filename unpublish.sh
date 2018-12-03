#!/bin/bash -e

VERSION=$1

source regions.sh

MD5SUM=$(md5 -q pypy35.zip)
S3KEY="pypy3.5/${MD5SUM}"

for region in "${PYPY35_REGIONS[@]}"; do
  bucket_name="iopipe-layers-${region}"

  echo "Deleting Lambda Layer pypy3.5 version ${VERSION} in region ${region}..."
  aws --region $region lambda delete-layer-version --layer-name pypy3.5 --version-number $VERSION
  echo "Deleted Lambda Layer pypy3.5 version ${VERSION} in region ${region}"
done
