package:
	sam package \
		--template-file template.yml \
		--output-template-file packaged.yml \
		--s3-bucket iopipe-pypy35-examples-us-east-1 \
		--region us-east-1

deploy: package
	aws cloudformation deploy \
		--template-file packaged.yml \
		--stack-name iopipe-pypy35-example-sam \
		--capabilities CAPABILITY_IAM \
		--region us-east-1
