from flask import Blueprint, jsonify
from db import query_db
from errors import IDNotFoundError


customers_get = Blueprint("customers_get", __name__)


@customers_get.route("", methods=["GET"])
def get_customers_list():
    """
    GET [API_URL]/customers

    Retrieve the customers list

    :return: list of customers
    """
    return jsonify(
        query_db("SELECT * FROM customers")
    )


@customers_get.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    """
    GET [API_URL]/customers/<customer_id>

    Retrieve the customer from ID

    :param customer_id: ID of customer
    :return: dict of customer
    :raise: IDNotFoundError if customer not found
    """
    customer = query_db("SELECT * FROM customers WHERE id=?", (customer_id,), True)
    if customer:
        return jsonify(customer)
    else:
        raise IDNotFoundError()
