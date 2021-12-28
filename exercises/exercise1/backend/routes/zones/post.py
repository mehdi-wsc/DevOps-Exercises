import json
from flask import Blueprint, jsonify
from db import query_db
from decorators import mandatory_post_fields
from errors import InsertError, InvalidFieldError


zones_post = Blueprint("zones_post", __name__)


@zones_post.route("", methods=["POST"])
@mandatory_post_fields("name", "polygon_json")
def create_zone(name, polygon_json):
    try:
        polygon = json.loads(polygon_json)
    except ValueError:
        raise InvalidFieldError("polygon_json")

    if type(polygon) != list or len(polygon) == 0:
        raise InvalidFieldError("polygon_json")
    for p in polygon:
        if type(p) != list or len(p) != 2:
            raise InvalidFieldError("polygon_json")

    zone_id = query_db("INSERT INTO zones (name, polygon) VALUES(?, ?)", (
        name,
        polygon_json
    ))
    if zone_id:
        return jsonify(query_db("SELECT * FROM zones WHERE id=?", (zone_id,), True))
    else:
        raise InsertError()
