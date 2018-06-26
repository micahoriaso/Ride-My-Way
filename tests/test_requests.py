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
    }
}


def test_get_all_requests(client):
    response = client.get('/api/v1/rides/2/requests')
    assert response.status_code == 200

def test_add_new_ride_offer_request(client):
    response = client.post('/api/v1/rides/2/requests', data = json.dumps(data['3']), headers=headers) 
    assert response.status_code == 201

def test_edit_existing_ride_offer_request(client):
    response = client.post('/api/v1/rides/2/requests',
                           data=json.dumps(data['3']), headers=headers)
    response = client.put(
        '/api/v1/rides/2/requests/1', data=json.dumps(data['3']), headers=headers)
    assert response.status_code == 200

def test_delete_existing_ride_offer_request(client):
    response = client.post('/api/v1/rides/2/requests',
                           data=json.dumps(data['3']), headers=headers)
    response = client.delete('/api/v1/rides/2/requests/1')
    assert response.status_code == 200

def test_delete_nonexistent_ride_offer_request(client):
    response = client.delete('/api/v1/rides/2/requests/10')
    assert response.status_code == 404
