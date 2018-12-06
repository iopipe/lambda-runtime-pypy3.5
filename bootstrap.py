#!/opt/pypy/bin/pypy

import decimal
import json
import os
import site
import sys
import urllib.request as request
import time

HANDLER = os.getenv("_HANDLER")
RUNTIME_API = os.getenv("AWS_LAMBDA_RUNTIME_API")

for path in ["/opt/pypy", "/opt/pypy/site-packages"]:
    sys.path.insert(0, path)
    site.addsitedir(path)

if "LAMBDA_TASK_ROOT" in os.environ:
    sys.path.insert(0, os.environ["LAMBDA_TASK_ROOT"])
    site.addsitedir(os.environ["LAMBDA_TASK_ROOT"])


class LambdaContext(object):
    def __init__(self, request_id, invoked_function_arn, deadline_ms, trace_id):
        self.aws_request_id = request_id
        self.deadline_ms = deadline_ms
        self.function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
        self.function_version = os.getenv("AWS_LAMBDA_FUNCTION_VERSION")
        self.invoked_function_arn = invoked_function_arn
        self.log_group_name = os.getenv("AWS_LAMBDA_LOG_GROUP_NAME")
        self.log_stream_name = os.getenv("AWS_LAMBDA_LOG_STREAM_NAME")
        self.memory_limit_in_mb = os.getenv("AWS_LAMBDA_FUNCTION_MEMORY_SIZE")
        self.trace_id = trace_id
        if self.trace_id is not None:
            os.environ["_X_AMZN_TRACE_ID"] = self.trace_id

    def get_remaining_time_in_millis(self):
        if self.deadline_ms is not None:
            return time.time() * 1000 - int(self.deadline_ms)


def decimal_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


def init_error(message, type):
    details = {"errorMessage": message, "errorType": type}
    details = json.dumps(details).encode("utf-8")
    req = request.Request(
        "http://%s/2018-06-01/runtime/init/error" % RUNTIME_API,
        details,
        {"Content-Type": "application/json"},
    )
    with request.urlopen(req) as res:
        res.read()


def next_invocation():
    with request.urlopen(
        "http://%s/2018-06-01/runtime/invocation/next" % RUNTIME_API
    ) as res:
        request_id = res.getheader("lambda-runtime-aws-request-id")
        invoked_function_arn = res.getheader("lambda-runtime-invoked-function-arn")
        deadline_ms = res.getheader("lambda-runtime-deadline-ms")
        trace_id = res.getheader("lambda-runtime-trace-id")
        event_payload = res.read()
    event = json.loads(event_payload.decode("utf-8"))
    context = LambdaContext(request_id, invoked_function_arn, deadline_ms, trace_id)
    return request_id, event, context


def invocation_response(request_id, handler_response):
    if not isinstance(handler_response, (bytes, str)):
        handler_response = json.dumps(handler_response, default=decimal_serializer)
    if not isinstance(handler_response, bytes):
        handler_response = handler_response.encode("utf-8")
    req = request.Request(
        "http://%s/2018-06-01/runtime/invocation/%s/response"
        % (RUNTIME_API, request_id),
        handler_response,
        {"Content-Type": "application/json"},
    )
    with request.urlopen(req) as res:
        res.read()


def invocation_error(request_id, error):
    details = {"errorMessage": str(error), "errorType": type(error).__name__}
    details = json.dumps(details).encode("utf-8")
    req = request.Request(
        "http://%s/2018-06-01/runtime/invocation/%s/error" % (RUNTIME_API, request_id),
        details,
        {"Content-Type": "application/json"},
    )
    with request.urlopen(req) as res:
        res.read()


if __name__ == "__main__":
    for runtime_var in ["AWS_LAMBDA_RUNTIME_API", "_HANDLER"]:
        if runtime_var not in os.environ:
            init_error("%s environment variable not set" % runtime_var, "RuntimeError")
            sys.exit(1)

    try:
        module_path, handler_name = HANDLER.rsplit(".", 1)
    except ValueError:
        init_error("Improperly formated handler value: %s" % HANDLER, "ValueError")
        sys.exit(1)

    module_path = module_path.replace("/", ".")

    try:
        module = __import__(module_path)
    except ImportError:
        init_error("Failed to import module: %s" % module_path, "ImportError")
        sys.exit(1)

    try:
        handler = getattr(module, handler_name)
    except AttributeError:
        init_error(
            "No handler %s in module %s" % (handler_name, module_path), "AttributeError"
        )
        sys.exit(1)

    while True:
        request_id, event, context = next_invocation()

        try:
            handler_response = handler(event, context)
        except Exception as e:
            invocation_error(request_id, e)
        else:
            invocation_response(request_id, handler_response)
