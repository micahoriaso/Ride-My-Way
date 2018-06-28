import pytest, json

import flaskr

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

data = {
    '1': {
        'date': '12-06-2018',
        'time': '11:00',
        'pickup': 'Nyayo Stadium',
        'dropoff': 'Belle Vue',
        'price': '100',
        'capacity': '3',
        'available_seats': '1',
        'driver_id': 1,
        'car': 'Mazda MX5',
        'registration': 'KAA 987I'
    },
    '4':{
        'date': '12-06-2018',
        'time': '11:00',
        'pickup': 'Nyayo Stadium',
        'dropoff': 'Belle Vue',
        'price': '100',
        'capacity': '3',
        'available_seats': '1',
        'driver_id': 1,
        'car': 'Mazda MX5',
        'registration': 'KAA 987I'
        }
    }


def test_add_new_ride_offer(client):
    response = client.post('/api/v2/rides/', data = json.dumps(data['4']), headers=headers) 
    assert response.status_code == 201

def test_get_all_rides(client):
    response = client.get('/api/v2/rides/')
    assert response.status_code == 200

def test_get_one_available_ride(client):
    response = client.post('/api/v2/rides/', data=json.dumps(data['4']), headers=headers)
    response = client.get('/api/v2/rides/1')
    assert response.status_code == 200

def test_get_one_unavailable_ride(client):
    response = client.get('/api/v2/rides/555')
    assert response.status_code == 404

def test_edit_existing_ride_offer(client):
    response = client.put('/api/v2/rides/1', data = json.dumps(data['1']), headers=headers) 
    assert response.status_code == 200

def test_delete_existing_ride(client):
    response = client.delete('/api/v2/rides/1')
    assert response.status_code == 200

def test_delete_nonexistent_ride(client):
    response = client.delete('/api/v2/rides/555')
    assert response.status_code == 404
