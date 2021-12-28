import json


def test_get_order(client):
    response = client.get("/deliveries/1")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d['id'] == 1


def test_get_order_id_not_found(client):
    response = client.get("/deliveries/43534343")
    assert response.status_code == 404
    assert "GETDeliveriesIdNotFound" in response.data


def test_get_order_vehicles(client):
    response = client.get("/deliveries/1/vehicles")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list
    assert len(d) > 0
    for v in d:
        assert v['delivery_id'] == 1


def test_get_order_products(client):
    response = client.get("/deliveries/1/products")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list
    assert len(d) > 0
    for p in d:
        assert p['delivery_id'] == 1


def test_get_orders_list(client):
    response = client.get("/deliveries")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list


def test_get_orders_list_from_customer(client):
    response = client.get("/deliveries?customer_id=1")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list
    assert len(d) > 0
    for order in d:
        assert order['customer_id'] == 1


def test_get_orders_list_from_zone(client):
    response = client.get("/deliveries?zone_id=1")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list
    assert len(d) > 0
    for order in d:
        assert order['zone_id'] == 1


def test_get_orders_list_from_driver(client):
    response = client.get("/deliveries?driver_id=1")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list
    assert len(d) > 0
    for order in d:
        assert order['driver_id'] == 1


def test_get_orders_list_from_date(client):
    response = client.get("/deliveries?date=2018-10-11")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list
    assert len(d) > 0
    for order in d:
        assert order['schedule_date'].split(" ")[0] == "2018-10-11"


def test_post_order(client):
    response = client.post("/deliveries", data={
        "customer_id": 1,
        "driver_id": 1,
        "location": "4 rue des gravilliers",
        "schedule_date": "2018-10-29 12:00:00"
    })
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d['customer_id'] == 1
    assert d['driver_id'] == 1
    assert d['zone_id'] == 1
    assert d['location'] == "4 rue des gravilliers"
    assert d['schedule_date'] == "2018-10-29 12:00:00"


def test_post_order_vehicle(client):
    response = client.post("/deliveries/1/vehicle", data={
        "description": "Test vehicle",
        "product_id": 1,
        "quantity": 99
    })
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d['description'] == "Test vehicle"
    assert d['delivery_id'] == 1
    assert d['product_id'] == 1
    assert d['quantity'] == 99


def test_post_order_vehicle_wrong_product(client):
    response = client.post("/deliveries/1/vehicle", data={
        "description": "Test vehicle",
        "product_id": 9999,
        "quantity": 99
    })
    assert response.status_code == 404
    assert "POSTDeliveriesProductIdNotFound" in response.data


def test_post_order_vehicle_wrong_order(client):
    response = client.post("/deliveries/98989898/vehicle", data={
        "description": "Test vehicle",
        "product_id": 1,
        "quantity": 99
    })
    assert response.status_code == 400
    assert "POSTDeliveriesProductInsertionFailed" in response.data


def test_post_order_missing_customer_id(client):
    response = client.post("/deliveries", data={
        "driver_id": 1,
        "location": "4 rue des gravilliers",
        "schedule_date": "2018-10-29 12:00:00"
    })
    assert response.status_code == 400
    assert "POSTDeliveriesCustomerIdMissing" in response.data


def test_post_order_missing_driver_id(client):
    response = client.post("/deliveries", data={
        "customer_id": 1,
        "location": "4 rue des gravilliers",
        "schedule_date": "2018-10-29 12:00:00"
    })
    assert response.status_code == 400
    assert "POSTDeliveriesDriverIdMissing" in response.data


def test_post_order_missing_location(client):
    response = client.post("/deliveries", data={
        "customer_id": 1,
        "driver_id": 1,
        "schedule_date": "2018-10-29 12:00:00"
    })
    assert response.status_code == 400
    assert "POSTDeliveriesLocationMissing" in response.data


def test_post_order_missing_date(client):
    response = client.post("/deliveries", data={
        "customer_id": 1,
        "driver_id": 1,
        "location": "4 rue des gravilliers"
    })
    assert response.status_code == 400
    assert "POSTDeliveriesScheduleDateMissing" in response.data


def test_post_order_wrong_customer(client):
    response = client.post("/deliveries", data={
        "customer_id": 9999,
        "driver_id": 1,
        "location": "4 rue des gravilliers",
        "schedule_date": "2018-10-29 12:00:00"
    })
    assert response.status_code == 400
    assert "POSTDeliveriesInsertionFailed" in response.data


def test_post_order_wrong_driver(client):
    response = client.post("/deliveries", data={
        "driver_id": 9999,
        "customer_id": 1,
        "location": "4 rue des gravilliers",
        "schedule_date": "2018-10-29 12:00:00"
    })
    assert response.status_code == 400
    assert "POSTDeliveriesInsertionFailed" in response.data


def test_post_order_not_in_zone(client):
    response = client.post("/deliveries", data={
        "driver_id": 9999,
        "customer_id": 1,
        "location": "Aix-En-Provence",
        "schedule_date": "2018-10-29 12:00:00"
    })
    assert response.status_code == 400
    assert "POSTDeliveriesInsertionFailed" in response.data
    assert "Location is not in a zone" in response.data
