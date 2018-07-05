import pytest, json

import flaskr

from flaskr.resources.helpers import get_db_rows

@pytest.fixture
def test_case_data():
    data = {
        '1': {
            "firstname": "Micah",
            "lastname": "Oriaso",
            "email": "micahoriaso@gmail.com",
            "password": "10101010",
            "confirm_password": "10101010"
        },
        '2': {
            "email": "micahoriaso@gmail.com",
            "password": "10101010",
        },
        '3': {
            "email": "micahoriaso@gmail.com",
            "password": "101010101",
        },
        '4': {
            "firstname": "Mike",
            "lastname": "Mike",
            "phone_number": "0777895621",
            "password": "10101010",
        },
        '5': {
            "firstname": "Sharon",
            "lastname": "Paul",
            "email": "sp@gmail.com",
            "password": "10101010",
            "confirm_password": "10101010"
        },
    }
    return data

def test_signup(client, test_case_data, header):
    pre_insert_rows = get_db_rows('select * from app_user;')
    response = client.post('/api/v2/auth/signup', 
                           data=json.dumps(test_case_data['5']), headers=header)
    post_insert_rows = get_db_rows('select * from app_user;')
    assert response.status_code == 201
    assert len(post_insert_rows) == len(pre_insert_rows) + 1

def test_edit_user(client, test_case_data, auth_header):
    response = client.put(
        '/api/v2/users/1', 
        data=json.dumps(test_case_data['4']), 
        headers=auth_header
        )
    assert response.status_code == 200

def test_get_one_existing_user(client, test_case_data, auth_header):
    response = client.get(
        '/api/v2/users/1', 
        headers=auth_header
        )
    assert response.status_code == 200


def test_get_one_nonexisting_user(client, test_case_data, auth_header):
    response = client.get(
        '/api/v2/users/900', 
        headers=auth_header
        )
    assert response.status_code == 404


def test_delete_nonexistent_user(client, test_case_data, auth_header):
    response = client.delete(
        '/api/v2/users/555', 
        headers=auth_header
        )
    assert response.status_code == 404


def test_delete_existing_user(client, test_case_data, auth_header):
    pre_delete_rows = get_db_rows('select * from app_user;')
    response = client.delete(
        '/api/v2/users/1', 
        headers=auth_header
        )
    post_delete_rows = get_db_rows('select * from app_user;')

    assert response.status_code == 200
    assert len(post_delete_rows) == len(pre_delete_rows) - 1

def test_login_with_good_credentials(client, test_case_data, header):
    response = client.post(
        '/api/v2/auth/login',
        data=json.dumps(test_case_data['2']), 
        headers=header
        )
    response_data = response.get_json()
    assert response_data['access_token'] is not None
    assert response.status_code == 200


def test_login_with_bad_credentials(client, test_case_data, header):
    response = client.post(
        '/api/v2/auth/login',
        data=json.dumps(test_case_data['3']), 
        headers=header
        )
    assert response.status_code == 202
