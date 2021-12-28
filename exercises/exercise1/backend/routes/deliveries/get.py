from flask import Blueprint, jsonify
from db import query_db
from decorators import get_fields
from errors import IDNotFoundError


deliveries_get = Blueprint("deliveries_get", __name__)


@deliveries_get.route("", methods=["GET"])
@get_fields("customer_id", "driver_id", "zone_id", "date")
def get_orders(customer_id, driver_id, zone_id, date):
    where_param = {}
    if zone_id is not None:
        where_param["d.zone_id"] = zone_id
    if driver_id is not None:
        where_param["d.driver_id"] = driver_id
    if customer_id is not None:
        where_param["d.customer_id"] = customer_id
    if date is not None:
        where_param["DATE(d.schedule_date)"] = date
    query = "SELECT d.*, "\
            "c.first_name AS customer_first_name, c.last_name AS customer_last_name, c.email AS customer_email, "\
            "dr.first_name AS driver_first_name, dr.last_name AS driver_last_name, dr.email AS driver_email, "\
            "z.name as zone_name " \
            "FROM deliveries d "\
            "LEFT OUTER JOIN customers c ON c.id=d.customer_id " \
            "LEFT OUTER JOIN drivers dr ON dr.id=d.driver_id " \
            "LEFT OUTER JOIN zones z ON z.id=d.zone_id"
    if len(where_param.keys()) > 0:
        query += " WHERE " + " AND ".join([k + "=?" for k in where_param.keys()])
    return jsonify(query_db(query, tuple(where_param.values())))


@deliveries_get.route("/<order_id>", methods=["GET"])
def get_order(order_id):
    order = query_db(
        "SELECT d.*, "
        "c.first_name AS customer_first_name, c.last_name AS customer_last_name, c.email AS customer_email, "
        "dr.first_name AS driver_first_name, dr.last_name AS driver_last_name, dr.email AS driver_email, "
        "z.name as zone_name "
        "FROM deliveries d "
        "LEFT OUTER JOIN customers c ON c.id=d.customer_id "
        "LEFT OUTER JOIN drivers dr ON dr.id=d.driver_id "
        "LEFT OUTER JOIN zones z ON z.id=d.zone_id "
        "WHERE d.id=?",
        (order_id,),
        True
    )
    if order:
        return jsonify(order)
    else:
        raise IDNotFoundError()


@deliveries_get.route("/<order_id>/vehicles", methods=["GET"])
def get_order_vehicles(order_id):
    return jsonify(query_db(
        "SELECT dv.*, dp.name as product_name, dp.price_ht as product_price_ht "
        "FROM deliveries_vehicles dv "
        "LEFT OUTER JOIN deliveries_products dp ON dp.id=dv.product_id "
        "WHERE dv.delivery_id=?",
        (order_id,)
    ))


@deliveries_get.route("/<order_id>/products", methods=["GET"])
def get_order_prices(order_id):
    return jsonify(query_db("SELECT * FROM deliveries_products WHERE delivery_id=?", (order_id,)))
