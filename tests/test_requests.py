import pytest, json
import flaskr

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

data = {
    "1": {
        "requestor_id": 1,
        "requestor_name": "Cynthia West",
        "request_status": "Accepted",
    },
    "2": {
        "requestor_id": 2,
        "requestor_name": "Mark Maasai",
        "request_status": "Declined",
    },
    "3": {
        "requestor_id": 3,
        "requestor_name": "Sadeeq Shaban",
        "request_status": "Accepted",
    }
}

def test_get_all_requests(client):
    response = client.get('/api/v1/rides/2/requests')
    assert response.status_code == 200

def test_add_new_ride_offer_request(client):
    response = client.post('/api/v1/rides/2/requests', data = json.dumps(data['3']), headers=headers) 
    assert response.status_code == 201

def test_add_existing_ride_offer_request(client):
    response = client.post('/api/v1/rides/2/requests', data = json.dumps(data['1']), headers=headers) 
    assert response.status_code == 406