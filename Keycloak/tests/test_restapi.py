import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from decouple import config as decouple_config

from api.restapi import app

client = TestClient(app)


def test_public_api():
    response = client.get('/api/v1/public')
    assert response.status_code == 200
    assert response.json() == {"message": "This is a public resource for everyone."}


def test_protected_admin_endpoint():
    load_dotenv()
    acc_token = os.environ.get('token_user1')
    _headers = {"Authorization": f"Bearer {acc_token}"}
    response = client.get('/api/v1/admin', headers=_headers)
    print(response.headers)
    assert response.status_code == 200
    assert response.json() == {"message": "This is a protected resource for ADMIN role."}


def test_protected_resource_path():
    load_dotenv()
    acc_token = os.environ.get('token_user1')
    location: str = "bergen"
    headers = {"Authorization": f'Bearer {acc_token}'}
    response = client.get(f'/api/v1/{location}', headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "message": f'This is a protected resource for any user that is registered on location = {location}.'}


def test_protected_resource_path_parameters():
    load_dotenv()
    acc_token = os.environ.get('token_user2')
    headers = {"Authorization": f'Bearer {acc_token}'}
    query: str = "param=bergen"
    response = client.get(f'/api/v1/?{query}', headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "message": f'This is a protected resource for any user that is registered on a location.'}