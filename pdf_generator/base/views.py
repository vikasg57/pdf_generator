import re

from django.utils.html import strip_tags
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework.views import APIView

from .exceptions import BaseAPIException


class AbstractAPIView(APIView):
    """Base API view used across the board."""

    def get_bool_query_value(self, param_str):
        value = self.request.GET.get(param_str)
        if value == 'false' or value == 'False' or not value:
            return False
        return True

    def get_bool_value_from_string(self, value):
        if value == 'false' or value == 'False' or not value:
            return False
        return True

    def get_sanitized_string(self, data_string, is_param_str=False):
        start_url_pattern = r'(?:http://\S+|https://\S+|www\.\S+)'
        end_url_pattern = r'\S+(?:\.com|\.org|\.net|\.gov|\.edu|\.mil|\.int|\.uk|\.ca|\.au|\.in|\.de|\.jp|\.fr|\.it|' \
                          r'\.es|\.nl|\.se|\.no|\.dk|\.br|\.ru|\.cn|\.kr|\.sg|\.hk|\.tw|\.io|\.me|\.info|\.biz|' \
                          r'\.coop|\.museum|\.aero|\.name)'
        match_symbol_pattern = r'[\{\}\[\]\(\)://<>]'
        if is_param_str:
            string = self.request.GET.get(data_string)
        else:
            string = self.request.data.get(data_string)
        if string:
            string = strip_tags(string)
            string = re.sub(start_url_pattern, '', string)
            string = re.sub(end_url_pattern, '', string)
            string = re.sub(match_symbol_pattern, '', string)
            string = string.strip()
            return string

    def get_email(self, email):
        if email is not None:
            try:
                validate_email(email)
            except Exception as e:
                raise BaseAPIException(
                    'Enter a valid email address.', 'validation_failed'
                )
        return email
