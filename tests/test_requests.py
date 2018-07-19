import pytest, json

import flaskr
from flaskr.resources.helpers import get_db_rows
from flaskr.models.user import User

@pytest.fixture
def test_case_data(client, auth_header, header):
    data = {
        '1': {
            'requestor_id': 1,
        },
        '2': {
            'requestor_id': 2,
        },
        '3': {
            'request_status': 'Accepted'
        },
        '4': {
            'date': '2018-06-12',
            'time': '11:00',
            'pickup': 'Nyayo Stadium',
            'dropoff': 'Belle Vue',
            'price': '100',
            'driver_id': 1,
        },
        '5': {
            "firstname": "Sharon",
            "lastname": "Paul",
            "email": "sp@gmail.com",
            "password": "10101010",
            "confirm_password": "10101010"
        },
        '6': {
            'registration': 'KAA 540H',
            'model': 'Nissan GTR',
            'capacity': '2',
        },
        '7': {
            "firstname": "Sharon",
            "lastname": "Paul",
            "password": "10101010",
            "car_registration": "KAA 540H",
            "phone_number": "0707896325"
        },
        '8': {
            'request_status': 'Not Accepted'
        },
        '9': {
            'requestor_id': 777,
        },
    }

    client.post('/api/v2/auth/signup',
        data=json.dumps(data['5']), headers=header)
    
    client.post(
        '/api/v2/cars/',
        data=json.dumps(data['6']), 
        headers=auth_header
        )

    client.put(
        '/api/v2/users/1',
        data=json.dumps(data['7']), 
        headers=auth_header)

    client.post(
        '/api/v2/rides/',
        data=json.dumps(data['4']), 
        headers=auth_header
        )

    return data


def test_get_empty_ride_request(client, test_case_data, auth_header):
    response = client.get('/api/v2/rides/1/requests',
                          headers=auth_header)
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['message'] == 'No requests available for this ride yet'

def test_add_new_ride_offer_request(client, test_case_data, auth_header):
    pre_insert_rows = get_db_rows('select * from ride_request;')
    response = client.post(
        '/api/v2/rides/1/requests', 
        data=json.dumps(test_case_data['1']), 
        headers=auth_header
        )
    post_insert_rows = get_db_rows('select * from ride_request;')

    assert len(post_insert_rows) == len(pre_insert_rows) + 1
    assert response.status_code == 201

def test_add_new_ride_offer_request_with_non_existing_requestor(client, test_case_data, auth_header):
    pre_insert_rows = get_db_rows('select * from ride_request;')
    response = client.post(
        '/api/v2/rides/1/requests', 
        data=json.dumps(test_case_data['9']), 
        headers=auth_header
        )
    post_insert_rows = get_db_rows('select * from ride_request;')

    response_data = response.get_json()
    assert len(post_insert_rows) == len(pre_insert_rows)
    assert response.status_code == 404
    assert 'The user with id {} does not exist'.format(
        test_case_data['9']['requestor_id']) in response_data['message']

def test_get_all_requests(client, auth_header):
    response = client.get(
        '/api/v2/rides/1/requests', 
        headers=auth_header
        )
    assert response.status_code == 200

def test_get_all_requests_for_nonexisting_ride(client, auth_header):
    response = client.get(
        '/api/v2/rides/77887/requests', 
        headers=auth_header
        )
    response_data = response.get_json()
    assert response.status_code == 404
    assert 'The ride with id {} does not exist'.format(
        77887) in response_data['message']

def test_get_nonexisting_ride_request(client, auth_header):
    response = client.get(
        '/api/v2/rides/1/requests/77887', 
        headers=auth_header
        )
    response_data = response.get_json()
    assert response.status_code == 404
    assert 'The ride request with id {} does not exist'.format(
        77887) in response_data['message']


def test_get_ride_request_details(client, auth_header, test_case_data):
    response = client.get(
        '/api/v2/rides/1/requests/1', 
        headers=auth_header
        )
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['data'][0]['ride_id'] == 1
    assert response_data['data'][0]['requestor'] == User.read(
        test_case_data['1']['requestor_id'])['fullname']
    assert response_data['data'][0]['request_status'] == 'Requested'


def test_edit_existing_ride_offer_request(client, test_case_data, auth_header):
    response = client.put(
        '/api/v2/rides/1/requests/1', 
        data=json.dumps(test_case_data['3']), 
        headers=auth_header
        )
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['data'] == 'Ride request successfully updated'

def test_edit_ride_offer_request_with_invalid_status(client, test_case_data, auth_header):
    response = client.put(
        '/api/v2/rides/1/requests/1', 
        data=json.dumps(test_case_data['8']), 
        headers=auth_header
        )
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['message'] == 'You entered an invalid request status'

def test_delete_existing_ride_offer_request(client, test_case_data, auth_header):
    pre_delete_rows = get_db_rows('select * from ride_request;')
    response = client.delete(
        '/api/v2/rides/1/requests/1', 
        headers=auth_header
        )
    post_delete_rows = get_db_rows('select * from ride_request;')

    assert len(post_delete_rows) == len(pre_delete_rows) - 1
    assert response.status_code == 200

def test_delete_nonexistent_ride_offer_request(client, auth_header):
    pre_delete_rows = get_db_rows('select * from ride_request;')
    response = client.delete(
        '/api/v2/rides/1/requests/20', 
        headers=auth_header
        )
    post_delete_rows = get_db_rows('select * from ride_request;')

    assert len(post_delete_rows) == len(pre_delete_rows)
    assert response.status_code == 404


def test_delete_request_from_nonexistent_ride_offer(client, auth_header):
    pre_delete_rows = get_db_rows('select * from ride_request;')
    response = client.delete(
        '/api/v2/rides/200/requests/1', 
        headers=auth_header
        )
    post_delete_rows = get_db_rows('select * from ride_request;')

    assert len(post_delete_rows) == len(pre_delete_rows)
    assert response.status_code == 404
