from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class EmailValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Email already exists.')
    default_code = 'email_exists'



class RegisterDisabledValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Register disabled.')
    default_code = 'register_disabled'


