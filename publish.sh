#!/bin/bash -e

source regions.sh

MD5SUM=$(md5 -q pypy35.zip)
S3KEY="pypy3.5/${MD5SUM}"

for region in "${PYPY35_REGIONS[@]}"; do
  bucket_name="iopipe-layers-${region}"

  echo "Publishing Lambda Layer pypy35 in region ${region}..."
  version=$(aws --region $region lambda publish-layer-version --cli-input-json "{\"LayerName\": \"pypy3.5\", \"Description\": \"PyPy 3.5 Lambda Runtime\", \"Content\": {\"S3Bucket\": \"${bucket_name}\", \"S3Key\": \"${S3KEY}\"}, \"CompatibleRuntimes\": [\"provided\"], \"LicenseInfo\": \"https://bitbucket.org/pypy/pypy/src/default/LICENSE?fileviewer=file-view-default\"}" --output text --query Version)
  echo "Published Lambda Layer pypy3.5 in region ${region} version ${version}"

  echo "Setting public permissions on Lambda Layer pypy3.5 version ${version} in region ${region}..."
  aws --region $region lambda add-layer-version-permission --layer-name pypy3.5 --version-number $version --statement-id=public --action lambda:GetLayerVersion --principal '*'
  echo "Public permissions set on Lambda Layer pypy3.5 version ${version} in region ${region}"
done
