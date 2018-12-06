# lambda-runtime-pypy3.5

An AWS Lambda Runtime for [PyPy 3.5](http://pypy.org)

## Overview

This is an AWS Lambda Runtime for PyPy 3.5. It uses [portable-pypy](https://github.com/squeaky-pl/portable-pypy), which is a statically-linked distribution of PyPy 3.5.

This runtime is still experimental and not intended for production use.

## Goals

* Make the runtime behave as closely to the `python3.6` runtime as possible.
* Improve runtime stability.
* Current runtime is 40MB zipped, 135MB unzipped. Reduce the runtime size by removing
  helpers/libraries that are included with portable-pypy that aren't relevant in an AWS
  Lambda use case.

## AWS Lambda Layers

This runtime is published as an [AWS LAmbda Layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html). If you're interested in giving it a try, here are the currently available ARNs:

* us-east-1: `arn:aws:lambda:us-east-1:146318645305:layer:pypy35:1`

More regions to come.

For an example of how to use AWS Lambda Layers, see this [SAM example](https://github.com/iopipe/lambda-runtime-pypy3.5/tree/master/examples/sam).

## Build

To build this runtime as a layer:

```bash
make pypy35.zip
```

## License

Apache 2.0