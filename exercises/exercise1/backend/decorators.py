from functools import wraps
from flask import request

from errors import MissingFieldError


def mandatory_post_fields(*fields):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            for field in fields:
                if field not in request.form.keys() or request.form[field] == '':
                    raise MissingFieldError(field)
                kwargs[field] = request.form[field]
            return f(*args, **kwargs)
        return decorated
    return wrapper


def get_fields(*fields):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            for field in fields:
                kwargs[field] = request.args.get(field)
            return f(*args, **kwargs)
        return decorated
    return wrapper