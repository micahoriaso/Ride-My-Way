import pytest, json

import flaskr

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

data = {
    '1': {
        'requestor_id': 1,
        'request_status': 'Pending'
    },
    '2': {
        'requestor_id': 2,
        'request_status': 'Accepted'
    },
    '3': {
        'requestor_id': 13,
        'request_status': 'Accepted'
    },
    '4': {
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

def test_add_new_ride_offer_request(client):
    client.post('/api/v2/rides/', data=json.dumps(data['4']), headers=headers)
    response = client.post('/api/v2/rides/1/requests', data = json.dumps(data['3']), headers=headers) 
    assert response.status_code == 201

def test_get_all_requests(client):
    response = client.get('/api/v2/rides/1/requests')
    assert response.status_code == 200


def test_edit_existing_ride_offer_request(client):
    response = client.post('/api/v2/rides/1/requests',
                           data=json.dumps(data['3']), headers=headers)
    response = client.put(
        '/api/v2/rides/1/requests/1', data=json.dumps(data['3']), headers=headers)
    assert response.status_code == 200

def test_delete_existing_ride_offer_request(client):
    response = client.post('/api/v2/rides/1/requests',
                           data=json.dumps(data['3']), headers=headers)
    response = client.delete('/api/v2/rides/1/requests/1')
    assert response.status_code == 200

def test_delete_nonexistent_ride_offer_request(client):
    response = client.delete('/api/v2/rides/1/requests/10')
    assert response.status_code == 404
