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


def test_signup(client):
    response = client.post('/api/v2/auth/signup', 
                            data = json.dumps(data['5']), headers = headers)
    assert response.status_code == 201

def test_edit_user(client):
    response = client.post('/api/v2/auth/signup',
                           data=json.dumps(data['1']), headers=headers)
    response = client.put(
        '/api/v2/users/2', data=json.dumps(data['4']), headers=headers)
    assert response.status_code == 200

def test_get_one_existing_user(client):
    response = client.post('/api/v2/auth/signup',
                           data=json.dumps(data['1']), headers=headers)
    response = client.get('/api/v2/users/1')
    assert response.status_code == 200

def test_get_one_nonexisting_user(client):
    response = client.get('/api/v2/users/900')
    assert response.status_code == 404

def test_delete_nonexistent_user(client):
    response = client.delete('/api/v2/users/555')
    assert response.status_code == 404

def test_delete_existing_user(client):
    response = client.delete('/api/v2/users/1')
    assert response.status_code == 200

def test_login_with_good_credentials(client):
    response = client.post('/api/v2/auth/login',
                           data=json.dumps(data['2']), headers=headers)
    assert response.status_code == 200

def test_login_with_bad_credentials(client):
    response = client.post('/api/v2/auth/login',
                           data=json.dumps(data['3']), headers=headers)
    assert response.status_code == 202
