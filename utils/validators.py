import re

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


_name_pattern = re.compile(r'^[a-zA-Z0-9_-]+$')
_url_validation = URLValidator()

def name_validator(value):

    if not _name_pattern.match(value):
        return ValidationError("invalid username")
    return True


def tag_validator(value: list):

    for x in value:
        if not re.match('^[a-zA-Z0-9_]+$', x.strip()):
            return ValidationError("invalid tags")

    return True


def url_validator(value):

    try:
        _url_validation(value)
        return True
    
    except ValidationError:
        return "invalid url"