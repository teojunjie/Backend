import logging

from rest_framework.response import Response
from rest_framework import status
from jsonschema.exceptions import ValidationError


class _BadRequestException(Exception):
    def __init__(self, message, reason_code=None):
        self.reason_code = reason_code
        super().__init__(message)


def validation_decorator(view):
    def _wrapped_view(request, *args, **kwargs):
        try:
            response = view(request, *args, **kwargs)
        except (ValidationError, _BadRequestException) as e:
            logging.warning(
                'validation/value error thrown',
                exc_info=True,
                extra=dict(
                    data=dict(
                        path=request.request.path
                        if hasattr(request, 'request')
                        and request.request.path else request.path,
                        exc_str=str(e),
                        exc_dict=e.__dict__,
                    ),
                ),
            )
            message = 'Your request was malformed. Please try again.'
            if e.__class__ not in (ValidationError, ValueError):
                message = str(e)
            response = dict(error=dict(message=message,
                                       client_message=message))
            if hasattr(e, 'reason_code'):
                response['error']['reason_code'] = e.reason_code
            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response
    return _wrapped_view
