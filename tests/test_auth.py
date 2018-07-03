import pytest, json

import flaskr

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
    response = client.post('/api/v2/auth/signup', 
                           data=json.dumps(test_case_data['5']), headers=header)
    assert response.status_code == 201

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
    response = client.delete(
        '/api/v2/users/1', 
        headers=auth_header
        )
    assert response.status_code == 200

def test_login_with_good_credentials(client, test_case_data, header):
    response = client.post(
        '/api/v2/auth/login',
        data=json.dumps(test_case_data['2']), 
        headers=header
        )
    assert response.status_code == 200


def test_login_with_bad_credentials(client, test_case_data, header):
    response = client.post(
        '/api/v2/auth/login',
        data=json.dumps(test_case_data['3']), 
        headers=header
        )
    assert response.status_code == 202
