from fastapi.testclient import TestClient
# Import the app from the main file
from de import app
import json
client  = TestClient(app)
import requests

data = {'username': "johndoe", 'password': "secret"}

response_token = client.post('/token/', data=data)
access_token = response_token.json()["access_token"]

headers = {"Authorization": f"Bearer {access_token}"}

def test_get_project_suggestions():
    response = client.post("/get_project_suggestions/", headers = headers)
    assert response.status_code == 200
    # check if the response is a as expected 
    

def test_create_project():
    response = client.post("/create_project/", headers = headers)
    assert response.status_code == 200
    # check if the response is a as expected

def test_create_repo():
    response = client.post("/create_repo/", headers = headers)
    assert response.status_code == 200
    # check if the response is a as expected


def test_push_notebook():
    response = client.post("/push_notebook/", headers = headers)
    assert response.status_code == 200
    # check if the response is a as expected
