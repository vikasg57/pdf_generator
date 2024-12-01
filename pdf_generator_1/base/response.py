from rest_framework import status as http_status
from rest_framework.response import Response

from .constants import (
    CONTENT_TYPE_JSON,
    SUCCESS_KEY,
    RESPONSE_DATA_KEY,
    RESPONSE_ERROR_KEY
)


class APIResponse(Response):

    def __init__(self, data=None, status=http_status.HTTP_200_OK, success=None, content_type=CONTENT_TYPE_JSON, **kwargs):
        success = (http_status.is_success(status)
                   if success is None
                   else success)

        key = RESPONSE_DATA_KEY if success else RESPONSE_ERROR_KEY
        response_data = {
            SUCCESS_KEY: success,
            key: data
        }
        super(APIResponse, self).__init__(data=response_data,
                                          status=status,
                                          content_type=content_type,
                                          **kwargs)
