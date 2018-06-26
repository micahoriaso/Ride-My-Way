import pytest, json

import flaskr

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

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
    },
    '5': {
        "firstname": "Sharon",
        "lastname": "Paul",
        "email": "sp@gmail.com",
        "password": "10101010",
        "confirm_password": "10101010"
    },
}


def test_signup(client):
    response = client.post('/api/v1/auth/signup', data = json.dumps(data['5']), headers = headers)
    assert response.status_code == 201

