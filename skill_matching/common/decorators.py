import json
from functools import wraps
from common import api_exceptions


def validate_json_request(f):
    """
    Validate request json
    :param f:
    :return:
    """

    @wraps(f)
    def func(request, *args, **kwargs):
        if request.method in ["GET", "DELETE"]:
            return f(request, *args, **kwargs)
        if request.body is None:
            return api_exceptions.ParserError(errors="Parser Error")
        try:
            if request.method in ["POST", "PUT"]:
                json.loads(request.body)
                return f(request, *args, **kwargs)
            else:
                raise api_exceptions.MethodNotAllowed(method=request.method)
        except ValueError:
            raise api_exceptions.ParserError(errors="Parser Error")

    return func
