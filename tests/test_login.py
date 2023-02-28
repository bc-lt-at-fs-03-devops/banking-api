from bank_api.resources.login_resource import LOGIN_ENDPOINT
from bank_api.resources.users_resource import USERS_ENDPOINT
from flask import jsonify

# username = "calvarez"
# password = "123456"
# code = "12345678"

def test_login(client,test_user_model):

    login_json = {
        "username": "calvarez",
        "password": "123456",
        "code": "12345678"
    }
    response = client.post(f"{LOGIN_ENDPOINT}",json=login_json)
    assert response.status_code == 200

def test_username_not_exist(client,test_user_model):

    login_json = {
        "username": "wrongusername",
        "password": "123456",
        "code": "12345678"
    }
    response = client.post(f"{LOGIN_ENDPOINT}",json=login_json)
    assert response.status_code == 404

def test_wrong_password(client,test_user_model):
    login_json = {
        "username": "calvarez",
        "password": "wrongpassword",
        "code": "12345678"
    }
    response = client.post(f"{LOGIN_ENDPOINT}",json=login_json)
    assert response.status_code == 400

def test_wrong_code(client,test_user_model):
    login_json = {
        "username": "calvarez",
        "password": "123456",
        "code": "wrongcode"
    }
    response = client.post(f"{LOGIN_ENDPOINT}",json=login_json)
    assert response.status_code == 400
