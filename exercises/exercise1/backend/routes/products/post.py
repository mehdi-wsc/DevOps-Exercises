from flask import Blueprint, jsonify
from db import query_db
from decorators import mandatory_post_fields
from errors import InsertError, IDNotFoundError, InvalidFieldError


products_post = Blueprint("products_post", __name__)


@products_post.route("", methods=["POST"])
@mandatory_post_fields("name", "price_ht")
def create_product(name, price_ht):
    product_id = query_db("INSERT INTO products (name) VALUES(?)", (name,))
    if product_id:
        product_price_id = query_db("INSERT INTO products_prices (product_id, price_ht) VALUES(?, ?)", (
            product_id,
            price_ht
        ))
        if product_price_id:
            return jsonify(query_db(
                "SELECT p.*, pp.price_ht as price_ht, pp.created_at as price_created_at "
                "FROM products p "
                "LEFT OUTER JOIN ("
                "SELECT MAX(id) as id, product_id FROM products_prices GROUP BY product_id"
                ") _pp ON _pp.product_id=p.id "
                "LEFT OUTER JOIN products_prices pp ON _pp.id=pp.id "
                "WHERE p.id=?",
                (product_id,),
                True
            ))
        else:
            query_db("DELETE FROM products WHERE id=?", (product_id,))
            raise InsertError("Price", "Unable to insert product price. Product has been removed")
    else:
        raise InsertError()


@products_post.route("/<product_id>/price", methods=["POST"])
@mandatory_post_fields("price_ht")
def add_price_for_product(product_id, price_ht):
    product = query_db("SELECT id FROM products WHERE id=?", (product_id,), True)
    if product:
        price_id = query_db("INSERT INTO products_prices (product_id, price_ht) VALUES(?, ?)", (
            product_id,
            price_ht
        ))
        if price_id:
            return jsonify(query_db(
                "SELECT p.*, pp.price_ht as price_ht, pp.created_at as price_created_at "
                "FROM products p "
                "LEFT OUTER JOIN ("
                "SELECT MAX(id) as id, product_id FROM products_prices GROUP BY product_id"
                ") _pp ON _pp.product_id=p.id "
                "LEFT OUTER JOIN products_prices pp ON _pp.id=pp.id "
                "WHERE p.id=?",
                (product_id,),
                True
            ))
        else:
            raise InsertError("Price")
    else:
        raise IDNotFoundError()
