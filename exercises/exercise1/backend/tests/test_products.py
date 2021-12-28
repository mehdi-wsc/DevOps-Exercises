import json


def test_post_product(client):
    response = client.post("/products", data={
        "name": "Product Test",
        "price_ht": 1.89
    })
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d['name'] == "Product Test"
    assert d['price_ht'] == 1.89


def test_post_product_missing_name(client):
    response = client.post("/products", data={
        "price_ht": 1.77
    })
    assert response.status_code == 400
    assert "POSTProductsNameMissing" in response.data


def test_post_product_missing_price(client):
    response = client.post("/products", data={
        "name": "Test Product"
    })
    assert response.status_code == 400
    assert "POSTProductsPriceHtMissing" in response.data


def test_post_product_wrong_price_format(client):
    response = client.post("/products", data={
        "name": "Product Test",
        "price_ht": "BLABLA"
    })
    assert response.status_code == 400
    assert "POSTProductsPriceHtInvalid" in response.data


def test_post_product_price(client):
    response = client.post("/products/1/price", data={
        "price_ht": 25.0
    })
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d['id'] == 1
    assert d['price_ht'] == 25.0


def test_post_product_price_missing_price(client):
    response = client.post("/products/1/price", data={})
    assert response.status_code == 400
    assert "POSTProductsPriceHtMissing" in response.data


def test_post_product_price_wrong_format(client):
    response = client.post("/products/1/price", data={
        "price_ht": "BLABLA"
    })
    assert response.status_code == 400
    assert "POSTProductsPriceHtInvalid" in response.data


def test_post_product_price_id_not_found(client):
    response = client.post("/products/3432432/price", data={
        "price_ht": 13.45
    })
    assert response.status_code == 404
    assert "POSTProductsIdNotFound" in response.data
