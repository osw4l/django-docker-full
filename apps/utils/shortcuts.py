from django.shortcuts import _get_queryset
from rest_framework.exceptions import ParseError, PermissionDenied


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except:
        return None


def get_list_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        return None
    return obj_list


def raise_parse_error(key=None, value=None):
    raise ParseError({key: value})


def raise_error(message):
    raise ParseError({'message': message})


def raise_permission_error(message):
    raise PermissionDenied({'message': message})
