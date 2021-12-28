from flask import Blueprint, jsonify
from db import query_db
from decorators import mandatory_post_fields
from errors import InsertError, DuplicateError


customers_post = Blueprint("customers_post", __name__)


@customers_post.route("", methods=["POST"])
@mandatory_post_fields("first_name", "last_name", "email")
def create_customer(first_name, last_name, email):
    """
    POST [API_URL]/customers

    Create the customer from post data

    :param first_name: customer first name
    :param last_name: customer last name
    :param email: customer email, must be unique in DB

    :return: dict of created customer
    :raise: InsertError Problem with customer insertion
    """

    # TODO : Remove
    exists = query_db("SELECT * FROM customers WHERE email=?", (email,), True)
    print(exists)
    if exists:
        raise DuplicateError("email")
    # End Remove

    customer_id = query_db(
        "INSERT INTO customers (first_name, last_name, email) VALUES(?, ?, ?)", (
            first_name,
            last_name,
            email
        )
    )
    if customer_id is not False:
        return jsonify(query_db("SELECT * FROM customers WHERE id=?", (customer_id,), True))
    else:
        raise InsertError()
