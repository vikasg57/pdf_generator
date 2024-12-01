from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    pass


class PaymentAPIException(APIException):
    pass


class AuthAPIException(APIException):
    pass


class ForbiddenAPIException(APIException):
    pass


class TooManyRequestsException(APIException):
    pass
