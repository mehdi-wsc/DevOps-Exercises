import json


def test_get_driver(client):
    response = client.get("/drivers/1")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert "id" in d and d['id'] == 1


def test_get_driver_not_found(client):
    response = client.get("/drivers/34343")
    assert response.status_code == 404
    assert "GETDriversIdNotFound" in response.data


def test_get_drivers_list(client):
    response = client.get("/drivers")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list


def test_get_drivers_from_zone(client):
    response = client.get("/drivers?zone_id=1")
    d = json.loads(response.data)
    assert response.status_code == 200
    for driver in d:
        assert driver['zone_id'] == 1


def test_post_driver(client):
    response = client.post("/drivers", data={
        "first_name": "Driver",
        "last_name": "Test",
        "email": "driver.test@test.test",
        "zone_id": 1
    })
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d["first_name"] == "Driver"
    assert d["last_name"] == "Test"
    assert d["email"] == "driver.test@test.test"
    assert d["zone_id"] == 1


def test_post_driver_duplicate(client):
    response = client.post("/drivers", data={
        "first_name": "Driver 2",
        "last_name": "Test 2",
        "email": "driver.test@test.test",
        "zone_id": 1
    })
    assert response.status_code == 400
    assert "POSTDriversEmailDuplicate" in response.data


def test_post_driver_missing_first_name(client):
    response = client.post("/drivers", data={
        "last_name": "Driver",
        "email": "driver.test.missing@localhost.dd",
        "zone_id": 1
    })
    assert response.status_code == 400
    assert "POSTDriversFirstNameMissing" in response.data


def test_post_driver_missing_last_name(client):
    response = client.post("/drivers", data={
        "first_name": "Driver",
        "email": "driver.test.missing@localhost.dd",
        "zone_id": 1
    })
    assert response.status_code == 400
    assert "POSTDriversLastNameMissing" in response.data


def test_post_driver_missing_email(client):
    response = client.post("/drivers", data={
        "first_name": "Driver",
        "last_name": "Test",
        "zone_id": 1
    })
    assert response.status_code == 400
    assert "POSTDriversEmailMissing" in response.data


def test_post_driver_missing_zone(client):
    response = client.post("/drivers", data={
        "first_name": "Driver",
        "last_name": "Test",
        "email": "driver.test.missing@localhost.dd"
    })
    assert response.status_code == 400
    assert "POSTDriversZoneIdMissing" in response.data


def test_post_driver_wrong_zone(client):
    response = client.post("/drivers", data={
        "first_name": "Driver",
        "last_name": "Test",
        "email": "driver.test.missing@localhost.dd",
        "zone_id": 58885
    })
    assert response.status_code == 400
    assert "POSTDriversInsertionFailed" in response.data
