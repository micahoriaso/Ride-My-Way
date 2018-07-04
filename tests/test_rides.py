# import pytest, json

# import flaskr

# @pytest.fixture
# def test_case_data():
#     data = {
#         '1': {
#             'date': '12-06-2018',
#             'time': '11:00',
#             'pickup': 'Nyayo Stadium',
#             'dropoff': 'Belle Vue',
#             'price': '100',
#             'capacity': '3',
#             'available_seats': '1',
#             'driver_id': 1,
#             'car': 'Mazda MX5',
#             'registration': 'KAA 987I'
#         },
#         '4':{
#             'date': '12-06-2018',
#             'time': '11:00',
#             'pickup': 'Nyayo Stadium',
#             'dropoff': 'Belle Vue',
#             'price': '100',
#             'capacity': '3',
#             'available_seats': '1',
#             'driver_id': 1,
#             'car': 'Mazda MX5',
#             'registration': 'KAA 987I'
#             }
#         }
#     return data


# def test_add_new_ride_offer(client, test_case_data, auth_header):
#     response = client.post('/api/v2/rides/', 
#                            data=json.dumps(test_case_data['4']), headers=auth_header)
#     assert response.status_code == 201

# def test_get_all_rides(client, auth_header):
#     response = client.get('/api/v2/rides/', headers=auth_header)
#     assert response.status_code == 200

# def test_get_one_available_ride(client, test_case_data, auth_header):
#     response = client.post('/api/v2/rides/', 
#                            data=json.dumps(test_case_data['4']), headers=auth_header)
#     response = client.get('/api/v2/rides/1', headers=auth_header)
#     assert response.status_code == 200

# def test_get_one_unavailable_ride(client, auth_header):
#     response = client.get('/api/v2/rides/555', headers=auth_header)
#     assert response.status_code == 404


# def test_edit_existing_ride_offer(client, test_case_data, auth_header):
#     response = client.put('/api/v2/rides/1', 
#                           data=json.dumps(test_case_data['1']), headers=auth_header)
#     assert response.status_code == 200

# def test_delete_existing_ride(client, auth_header):
#     response = client.delete('/api/v2/rides/1', headers=auth_header)
#     assert response.status_code == 200

# def test_delete_nonexistent_ride(client, auth_header):
#     response = client.delete('/api/v2/rides/555', headers=auth_header)
#     assert response.status_code == 404
