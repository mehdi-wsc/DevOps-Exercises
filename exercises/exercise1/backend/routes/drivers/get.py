from flask import Blueprint, jsonify
from db import query_db
from decorators import get_fields
from errors import IDNotFoundError


drivers_get = Blueprint("drivers_get", __name__)


@drivers_get.route("", methods=["GET"])
@get_fields("zone_id")
def get_drivers_list(zone_id):
    """
    GET [API_URL]/drivers

    Retrieve drivers list.
    Can be filtered by zone

    :param zone_id: Zone id to filter drivers. Not mandatory. Default is None
    :return: Drivers list
    """
    where_param = {}
    if zone_id is not None:
        where_param["zone_id"] = zone_id
    query = "SELECT * FROM drivers"
    if len(where_param.keys()) > 0:
        query += " WHERE " + " AND ".join([k + "=?" for k in where_param.keys()])
    return jsonify(query_db(query, tuple(where_param.values())))


@drivers_get.route("/<driver_id>", methods=["GET"])
def get_driver(driver_id):
    """
    GET [API_URL]/drivers/<driver_id>

    Retrieve driver data from id

    :param driver_id: Driver id to retrieve
    :return: driver data
    :raise: IDNotFoundError
    """
    driver = query_db("SELECT * FROM drivers WHERE id=?", (driver_id,), True)
    if driver:
        return jsonify(driver)
    else:
        raise IDNotFoundError()
