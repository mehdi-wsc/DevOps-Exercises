from flask import request, jsonify


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class BaseApiError(Exception):
    def __init__(self, code, message="", sub_code="", details="", **kwargs):
        self.code = code
        self.message = message
        self.details = details
        self.method = request.method
        self.others = kwargs
        self.module = request.blueprint.split("_")[0].title() if request.blueprint else ""
        self.sub_code = self.method + self.module + sub_code

    def to_json(self):
        d = {
            "code": self.code,
            "message": self.message,
            "sub_code": self.sub_code,
            "details": self.details
        }
        if self.others:
            d.update(self.others)
        return jsonify(d)


class ServerError(BaseApiError):
    def __init__(self, details="", **kwargs):
        super(ServerError, self).__init__(500, "Internal server error", "ServerError", details, **kwargs)


class MissingFieldError(BaseApiError):
    def __init__(self, field_name, details="Field is missing", **kwargs):
        super(MissingFieldError, self).__init__(
            400, "Bad request", to_camel_case(field_name.capitalize()) + "Missing", details, **kwargs
        )


class InsertError(BaseApiError):
    def __init__(self, model="", details="Insertion failed", **kwargs):
        super(InsertError, self).__init__(
            400, "Bad request", to_camel_case(model.capitalize()) + "InsertionFailed", details, **kwargs
        )


class DuplicateError(BaseApiError):
    def __init__(self, field="", details="Duplicate field", **kwargs):
        super(DuplicateError, self).__init__(
            400, "Bad request", to_camel_case(field.capitalize()) + "Duplicate", details, **kwargs
        )


class IDNotFoundError(BaseApiError):
    def __init__(self, model="", details="Resource not found", **kwargs):
        super(IDNotFoundError, self).__init__(
            404, "Not found", to_camel_case(model.capitalize()) + "IdNotFound", details, **kwargs
        )


class InvalidFieldError(BaseApiError):
    def __init__(self, field_name, details="Field is invalid", **kwargs):
        super(InvalidFieldError, self).__init__(
            400, "Bad request", to_camel_case(field_name.capitalize()) + "Invalid", details, **kwargs
        )
