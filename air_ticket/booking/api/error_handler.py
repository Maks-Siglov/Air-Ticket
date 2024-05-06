from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc: Exception, context: dict) -> Response:

    response = exception_handler(exc, context)

    if response is not None and response.data is not None:
        print(response)
        print(response.data)
        response.data["status_code"] = response.status_code

    return response
