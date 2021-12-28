from flask import Blueprint, jsonify
from db import query_db
from decorators import mandatory_post_fields
from errors import InsertError, DuplicateError


drivers_post = Blueprint("drivers_post", __name__)


@drivers_post.route("", methods=["POST"])
@mandatory_post_fields("first_name", "last_name", "email", "zone_id")
def create_driver(first_name, last_name, email, zone_id):
    """
    POST [API_URL]/drivers

    Route to create a driver. Email must be unique

    :param first_name: Driver first name
    :param last_name: Driver last name
    :param email: Driver email. Must be unique
    :param zone_id: Zone associated to driver. Must exists in database

    :return: New driver data
    :raise: InsertError
    """
    exists = query_db("SELECT * FROM drivers WHERE email=?", (email,), True)
    if not exists:
        driver_id = query_db(
            "INSERT INTO drivers (first_name, last_name, email, zone_id) VALUES(?, ?, ?, ?)", (
                first_name,
                last_name,
                email,
                zone_id
            ),
            True
        )

        if driver_id is not False:
            return jsonify(query_db("SELECT * FROM drivers WHERE id=?", (driver_id,), True))
        else:
            raise InsertError()
    else:
        raise DuplicateError("email")
