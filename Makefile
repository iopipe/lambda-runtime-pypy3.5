SHELL=/bin/bash

all: clean pypy35.zip upload publish

pypy35.zip:
	./build.sh

upload: pypy35.zip
	./upload.sh

publish: pypy35.zip
	./publish.sh

clean:
	rm -rf layer pypy35.zip

shell:
	docker run --rm -v "$PWD":/opt lambci/lambda:build-provided sh
