import json


def test_get_zone(client):
    response = client.get("/zones/1")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert 'id' in d and d['id'] == 1


def test_get_zone_not_found(client):
    response = client.get("/zones/100000")
    assert response.status_code == 404
    assert 'GETZonesIdNotFound' in response.data


def test_get_zones_list(client):
    response = client.get("/zones")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert type(d) == list


def test_get_zone_from_lat_lng_1(client):
    response = client.get("/zones/geo/48.8640006,2.3540513")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d["id"] == 1


def test_get_zone_from_lat_lng_2(client):
    response = client.get("/zones/geo/50.6310623,3.0121412")
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d["id"] == 2


def test_get_zone_from_lat_lng_not_found(client):
    response = client.get("/zones/geo/43.5359526,5.3179078")
    assert response.status_code == 200
    assert "null\n" == response.data


def test_get_zone_from_wrong_lat_lng(client):
    response = client.get("/zones/geo/48.8640006_2.3540513")
    assert response.status_code == 400
    assert "GETZonesLatLngInvalid" in response.data


def test_get_zone_from_missing_lat_lng(client):
    response = client.get("/zones/geo/")
    assert response.status_code == 404
    assert "GETNotFound" in response.data


def test_post_zone(client):
    response = client.post("/zones", data={
        "name": "Test Zone",
        "polygon_json": json.dumps([
            [1, 1],
            [2, 2]
        ])
    })
    d = json.loads(response.data)
    assert response.status_code == 200
    assert d['name'] == "Test Zone"
    assert d['polygon'] == '[[1, 1], [2, 2]]'


def test_post_zone_missing_name(client):
    response = client.post("/zones", data={
        "polygon_json": json.dumps([
            [1, 1],
            [2, 2]
        ])
    })
    assert response.status_code == 400
    assert "POSTZonesNameMissing" in response.data


def test_post_zone_missing_polygon(client):
    response = client.post("/zones", data={
        "name": "Zone TEst 2"
    })
    assert response.status_code == 400
    assert "POSTZonesPolygonJsonMissing" in response.data


def test_post_zone_wrong_polygon(client):
    response = client.post("/zones", data={
        "name": "Test Zone 3",
        "polygon_json": json.dumps([1, 2])
    })
    assert response.status_code == 400
    assert "POSTZonesPolygonJsonInvalid" in response.data


def test_post_zone_wrong_polygon_2(client):
    response = client.post("/zones", data={
        "name": "Test Zone 3",
        "polygon_json": 'rete;fd[re'
    })
    assert response.status_code == 400
    assert "POSTZonesPolygonJsonInvalid" in response.data


def test_post_zone_wrong_polygon_point(client):
    response = client.post("/zones", data={
        "name": "Test Zone 3",
        "polygon_json": json.dumps([[1, 2], False])
    })
    assert response.status_code == 400
    assert "POSTZonesPolygonJsonInvalid" in response.data


def test_post_zone_wrong_polygon_point_2(client):
    response = client.post("/zones", data={
        "name": "Test Zone 3",
        "polygon_json": json.dumps([[1, 2], [1, 2, 3]])
    })
    assert response.status_code == 400
    assert "POSTZonesPolygonJsonInvalid" in response.data


def test_post_zone_empty_polygon(client):
    response = client.post("/zones", data={
        "name": "Test Zone 3",
        "polygon_json": json.dumps([])
    })
    assert response.status_code == 400
    assert "POSTZonesPolygonJsonInvalid" in response.data
