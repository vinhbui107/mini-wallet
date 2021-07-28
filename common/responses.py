from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


class ApiSuccessResponse(Response):
    def __init__(
        self,
        data,
        status=status.HTTP_200_OK,
    ):
        status_text = "success"
        if "error" in data:
            status_text = "fail"

        super().__init__(
            {"status": status_text, "data": data},
            status,
        )


class ApiErrorResponse(Response):
    def __init__(
        self,
        message,
        status=status.HTTP_200_OK,
    ):
        super().__init__({"status": "error", "message": message}, status)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        res = {"status": "fail", "data": response.data}
        response.data = res
    return response
