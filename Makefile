pypy35.zip:
	./build.sh

upload: pypy35.zip
	./upload.sh

publish: pypy35.zip
	./publish.sh

clean:
	rm pypy35.zip
