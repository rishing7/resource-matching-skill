from functools import wraps
from django.http import JsonResponse
from common.responses.erros import (
    BAD_REQUEST,
    SERVER_ERROR,
    PARSER_ERROR,
    METHOD_NOT_ALLOWED,
)


# most exception classes are a blatant ripoff, just shaved off some stuff:
# https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/exceptions.py
# exception_handler is a homegrown decorator,
# different from how DRF handles it.


def api_exception_handler(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        try:
            func = f(request, *args, **kwargs)
            return func
        except APIException as e:
            # api exceptions are of string typed error
            if isinstance(e.errors, str):
                error = e.errors

            # check if error is of dict type
            elif isinstance(e.errors, dict):
                error = dict()
                for k, v in e.errors.items():
                    # error can be dict of dict
                    if isinstance(v, dict):
                        # this error type handling nested schema, reference: check for register account errors
                        try:
                            error.update(
                                {
                                    str(k).lower(): {
                                        str(m).lower(): (
                                            e[0] if isinstance(e, list) else e
                                        )
                                        for m, e in v.items()
                                    }
                                }
                            )
                        # HACK: Exception to handle case in which parsing looks inappropriate.
                        # Need to find another way
                        # TODO: We need to check for multi language error in exception case.
                        except AttributeError:
                            error.update({str(k).lower(): v})
                    # if error dict values contains list , errors used everywhere in schema
                    else:
                        # msg = [",".join(v) if isinstance(v, list) else v]
                        error.update(
                            {str(k).lower(): v[0] if isinstance(v, list) else v}
                        )

            # if something unexpected happened
            else:
                error = e.errors
            return JsonResponse(
                {"message": str(e.detail), "error": error, "status_code": e.code},
                status=e.r_code,
            )

    return decorated_function


class APIException(Exception):
    """
    Base class for API exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """

    # default - for unhandled exceptions - should ideally never happen, since
    # these will be mostly raised by devs themselves while handling requests.
    status_code = 500
    default_detail = SERVER_ERROR

    def __init__(self, detail=None, errors=None, code=None, r_code=None):
        if detail is None:
            self.detail = self.default_detail
        else:
            self.detail = detail

        self.errors = errors

        if code is None:
            self.code = self.status_code
        else:
            self.code = code

        if r_code is None:
            self.r_code = self.code
        else:
            self.r_code = r_code

    def __str__(self):
        return self.detail


class BadRequestData(APIException):
    status_code = 400
    default_detail = BAD_REQUEST


class ParserError(APIException):
    status_code = 400
    default_detail = PARSER_ERROR


class MethodNotAllowed(APIException):
    status_code = 403
    default_detail = METHOD_NOT_ALLOWED
