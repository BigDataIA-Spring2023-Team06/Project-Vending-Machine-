from fastapi import FastAPI
from fastapi.testclient import TestClient
from de import app
import json

import requests
# app = FastAPI()
client  = TestClient(app)

data = {'username': "aryan", 'password': "secret"}


response_token = client.post('/token', params=data)   


access_token = response_token.json()
print(access_token)

headers = {"Authorization": f"Bearer {access_token}"}