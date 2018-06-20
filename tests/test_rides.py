import pytest, json
import flaskr

def test_get_all_rides(client):
    response = client.get('/api/v1/rides/')
    assert response.status_code == 200

def test_get_one_available_ride(client):
    response = client.get('/api/v1/rides/1')
    assert response.status_code == 200

def test_get_one_unavailable_ride(client):
    response = client.get('/api/v1/rides/555')
    assert response.status_code == 404
