import json
from flask import Blueprint, jsonify
from db import query_db
from helpers.geo import GeoHelper
from decorators import mandatory_post_fields
from errors import InsertError, IDNotFoundError


deliveries_post = Blueprint("deliveries_post", __name__)


@deliveries_post.route("", methods=["POST"])
@mandatory_post_fields("customer_id", "driver_id", "location", "schedule_date")
def create_order(customer_id, driver_id, location, schedule_date):
    lat, lng = GeoHelper.get_address_lat_lng(location)
    if lat and lng:
        zone_id = None
        for zone in query_db("SELECT * FROM zones"):
            if GeoHelper.point_inside_polygon(lng, lat, json.loads(zone['polygon'])):
                zone_id = zone["id"]
                break
        if not zone_id:
            raise InsertError(details="Location is not in a zone")
        order_id = query_db(
            "INSERT INTO deliveries "
            "(customer_id, driver_id, zone_id, lat, lng, location, schedule_date) "
            "VALUES(?, ?, ?, ?, ?, ?, ?)",
            (customer_id, driver_id, zone_id, lat, lng, location, schedule_date)
        )
        if order_id:
            prod_query = "SELECT p.*, pp.price_ht as price_ht "\
                "FROM products p "\
                "LEFT OUTER JOIN ("\
                "SELECT MAX(id) as id, product_id FROM products_prices GROUP BY product_id"\
                ") _pp ON _pp.product_id=p.id "\
                "LEFT OUTER JOIN products_prices pp ON _pp.id=pp.id"

            for product in query_db(prod_query):
                query_db(
                    "INSERT INTO deliveries_products (delivery_id, product_id, name, price_ht) VALUES(?, ?, ?, ?)",(
                    order_id,
                    product['id'],
                    product["name"],
                    product["price_ht"]
                ))

            return jsonify(query_db(
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
            ))
        else:
            raise InsertError()
    else:
        raise InsertError("Unable to retrieve location position")


@deliveries_post.route("/<order_id>/vehicle", methods=["POST"])
@mandatory_post_fields("product_id", "description", "quantity")
def add_order_vehicle(order_id, product_id, description, quantity):
    delivery_product = query_db(
        "SELECT dp.id FROM deliveries_products dp LEFT OUTER JOIN products p ON p.id=dp.product_id "
        "WHERE dp.delivery_id=? AND dp.product_id=?", (
            order_id,
            product_id
        ),
        True
    )
    if not delivery_product:
        product = query_db(
            "SELECT p.*, pp.price_ht as price_ht "
            "FROM products p "
            "LEFT OUTER JOIN ("
            "SELECT MAX(id) as id, product_id FROM products_prices GROUP BY product_id"
            ") _pp ON _pp.product_id=p.id "
            "LEFT OUTER JOIN products_prices pp ON _pp.id=pp.id "
            "WHERE p.id=?",
            (product_id,),
            True
        )
        if not product:
            raise IDNotFoundError("product")
        else:
            delivery_product_id = query_db(
                "INSERT INTO deliveries_products (delivery_id, product_id, name, price_ht) VALUES(?, ?, ?, ?)", (
                    order_id,
                    product['id'],
                    product["name"],
                    product["price_ht"]
                )
            )
            if not delivery_product_id:
                raise InsertError("Product")
    else:
        delivery_product_id = delivery_product['id']

    delivery_vehicle_id = query_db(
        "INSERT INTO deliveries_vehicles (delivery_id, product_id, description, quantity) VALUES(?, ?, ?, ?)", (
            order_id,
            delivery_product_id,
            description,
            quantity
        )
    )

    if delivery_vehicle_id:
        return jsonify(query_db(
            "SELECT dv.*, dp.name as product_name, dp.price_ht as product_price_ht "
            "FROM deliveries_vehicles dv "
            "LEFT OUTER JOIN deliveries_products dp ON dp.id=dv.product_id "
            "WHERE dv.id=?",
            (delivery_vehicle_id,),
            True
        ))
    else:
        raise InsertError("vehicle")
