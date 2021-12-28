from flask import Blueprint, jsonify
from db import query_db
from decorators import get_fields
from errors import IDNotFoundError


products_get = Blueprint("products_get", __name__)


@products_get.route("", methods=["GET"])
def get_products_list():
    """
    GET [API_URL]/products

    Retrieve products list.

    :return: Products list
    """
    where_param = {}
    query = "SELECT p.*, pp.price_ht as price_ht, pp.created_at as price_created_at "\
        "FROM products p "\
        "LEFT OUTER JOIN ("\
        "SELECT MAX(id) as id, product_id FROM products_prices GROUP BY product_id"\
        ") _pp ON _pp.product_id=p.id "\
        "LEFT OUTER JOIN products_prices pp ON _pp.id=pp.id "
    if len(where_param.keys()) > 0:
        query += " WHERE " + " AND ".join([k + "=?" for k in where_param.keys()])
    return jsonify(query_db(query, tuple(where_param.values())))


@products_get.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    """
    GET [API_URL]/product/<product_id>

    Retrieve product data from id

    :param product_id: Product id to retrieve
    :return: product data
    :raise: IDNotFoundError
    """
    product = query_db(
        "SELECT p.*, pp.price_ht as price_ht, pp.created_at as price_created_at "
        "FROM products p "
        "LEFT OUTER JOIN ("
        "SELECT MAX(id) as id, product_id FROM products_prices GROUP BY product_id"
        ") _pp ON _pp.product_id=p.id "
        "LEFT OUTER JOIN products_prices pp ON _pp.id=pp.id WHERE p.id=?", (product_id,), True)
    if driver:
        return jsonify(product)
    else:
        raise IDNotFoundError()
