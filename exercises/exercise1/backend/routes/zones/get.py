import json
from flask import Blueprint, jsonify
from db import query_db
from errors import IDNotFoundError, InvalidFieldError
from helpers.geo import GeoHelper


zones_get = Blueprint("zones_get", __name__)


@zones_get.route("", methods=["GET"])
def get_zones_list():
    """
    GET [API_URL]/zones

    Retrieve zones list

    :return: Zones list
    """
    return jsonify(query_db("SELECT * FROM zones"))


@zones_get.route("/<zone_id>", methods=["GET"])
def get_zone(zone_id):
    """
    GET [API_URL]/zones/<zone_id>

    Retrieve zone from ID

    :param zone_id: Zone ID
    :return: Zone data
    :raise: IDNotFoundError
    """
    zone = query_db("SELECT * FROM zones WHERE id=?", (zone_id,), True)
    if zone:
        return jsonify(zone)
    else:
        raise IDNotFoundError()


@zones_get.route("/geo/<lat_lng>", methods=["GET"])
def get_zone_from_lat_lng(lat_lng):
    """
    GET [API_URL]/zones/geo/<lat_lng>

    Check if a lat,lng position is in a zone.
    Return first zone found.

    :param lat_lng: latitude and longitude of a geo point. Format : lat,lng
    :return: First zone found or None if no zone found
    """
    zones = query_db("SELECT * FROM zones")
    try:
        lat, lng = map(float, lat_lng.split(","))
    except ValueError:
        raise InvalidFieldError("lat_lng")
    for zone in zones:
        if GeoHelper.point_inside_polygon(lng, lat, json.loads(zone['polygon'])):
            return jsonify(zone)
    return jsonify(None)
