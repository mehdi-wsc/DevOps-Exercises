import json


def test_get_customer(client):
    response = client.get('/customers/1')
    d = json.loads(response.data)
    assert response.status_code == 200
    assert "id" in d and d['id'] == 1


def test_get_customer_not_found(client):
    response = client.get("/customers/34343")
    assert response.status_code == 404
    assert "GETCustomersIdNotFound" in response.data


def test_get_customers_list(client):
    response = client.get("/customers")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list


def test_post_customer(client):
    response = client.post("/customers", data={
        "first_name": "Test",
        "last_name": "Customer",
        "email": "test.customer@test.test"
    })
    d = json.loads(response.data)
    print response.data
    assert response.status_code == 200
    assert "id" in d
    assert d["first_name"] == "Test"
    assert d["last_name"] == "Customer"
    assert d["email"] == "test.customer@test.test"


def test_post_customer_duplicate(client):
    response = client.post("/customers", data={
        "first_name": "Test 2",
        "last_name": "Customer 2",
        "email": "test.customer@test.test"
    })
    assert response.status_code == 400
    assert "POSTCustomersEmailDuplicate" in response.data


def test_post_customer_missing_email(client):
    response = client.post("/customers", data={
        "first_name": "Test 2",
        "last_name": "Customer 2"
    })
    assert response.status_code == 400
    assert "POSTCustomersEmailMissing" in response.data


def test_post_customer_missing_first_name(client):
    response = client.post("/customers", data={
        "last_name": "Customer 2",
        "email": "test2.customer@test.test"
    })
    assert response.status_code == 400
    assert "POSTCustomersFirstNameMissing" in response.data


def test_post_customer_missing_last_name(client):
    response = client.post("/customers", data={
        "first_name": "Test 2",
        "email": "test2.customer@test.test"
    })
    assert response.status_code == 400
    assert "POSTCustomersLastNameMissing" in response.data
