import pytest, json

import flaskr

@pytest.fixture
def test_case_data():
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
    return data


def test_add_new_ride_offer_request(client, test_case_data, auth_header):
    client.post(
        '/api/v2/rides/',
        data=json.dumps(test_case_data['4']), 
        headers=auth_header
        )
    response = client.post(
        '/api/v2/rides/1/requests', 
        data=json.dumps(test_case_data['3']), 
        headers=auth_header
        )
    assert response.status_code == 201

def test_get_all_requests(client, auth_header):
    response = client.get(
        '/api/v2/rides/1/requests', 
        headers=auth_header
        )
    assert response.status_code == 200

def test_edit_existing_ride_offer_request(client, test_case_data, auth_header):
    response = client.post(
        '/api/v2/rides/1/requests',
        data=json.dumps(test_case_data['3']), 
        headers=auth_header
        )
    response = client.put(
        '/api/v2/rides/1/requests/1', 
        data=json.dumps(test_case_data['3']), 
        headers=auth_header
        )
    assert response.status_code == 200

def test_delete_existing_ride_offer_request(client, test_case_data, auth_header):
    response = client.post(
        '/api/v2/rides/1/requests',
        data=json.dumps(test_case_data['3']), 
        headers=auth_header
        )
    response = client.delete(
        '/api/v2/rides/1/requests/1', 
        headers=auth_header
        )
    assert response.status_code == 200

def test_delete_nonexistent_ride_offer_request(client, auth_header):
    response = client.delete(
        '/api/v2/rides/1/requests/10', 
        headers=auth_header
        )
    assert response.status_code == 404
