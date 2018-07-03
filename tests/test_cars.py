import pytest, json

import flaskr

@pytest.fixture
def test_case_data():
    data = {
        '1': {
            'registration': 'KAA 540H',
            'model': 'Nissan GTR',
            'capacity': '1',
        },
        '2':{
            'model': 'BMW M5',
            'capacity': '3',
            }
        }
    return data


def test_add_new_car(client, test_case_data, auth_header):
    response = client.post('/api/v2/cars/', 
                           data=json.dumps(test_case_data['1']), headers=auth_header)
    assert response.status_code == 201

def test_get_all_cars(client, auth_header):
    response = client.get('/api/v2/cars/', headers=auth_header)
    assert response.status_code == 200

def test_get_one_available_car(client, test_case_data, auth_header):
    client.post('/api/v2/cars/', 
                           data=json.dumps(test_case_data['1']), headers=auth_header)
    response = client.get('/api/v2/cars/KAA 540H', headers=auth_header)
    assert response.status_code == 200

def test_get_one_unavailable_car(client, auth_header):
    response = client.get('/api/v2/cars/555', headers=auth_header)
    assert response.status_code == 404

def test_edit_existing_car(client, test_case_data, auth_header):
    response = client.put('/api/v2/cars/KAA 540H',
                          data=json.dumps(test_case_data['2']), headers=auth_header)
    assert response.status_code == 200

def test_delete_nonexistent_car(client, auth_header):
    response = client.delete('/api/v2/cars/555', headers=auth_header)
    assert response.status_code == 404

def test_delete_existing_car(client, auth_header):
    response = client.delete('/api/v2/cars/KAA 540H', headers=auth_header)
    assert response.status_code == 200
