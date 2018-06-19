import pytest, json
import flaskr

def test_index(client):
    response = client.get('/api/v1/rides/')
