import datetime

from bank_api.resources.account_resource import ACCOUNT_ENDPOINT
from bank_api.resources.login_resource import LOGIN_ENDPOINT


def test_create_account(client, test_user_model):

    login_json = {
        "username": "calvarez",
        "password": "123456",
        "code": "12345678"
    }
    login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
    assert login_response.status_code == 200
    account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                   headers={'Authorization': login_response.json['access_token']})

    assert account_response.status_code == 200


def test_create_account_without_auth(client):
    account_response = client.post(f"{ACCOUNT_ENDPOINT}")
    assert account_response.status_code == 401


def test_create_account_with_wrong_auth(client, test_user_model):
    login_json = {
        "username": "calvarez",
        "password": "123456",
        "code": "12345678"
    }
    login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
    account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                   headers={'Authorization': login_response.json['access_token']+'sd'})

    assert account_response.status_code == 422


def test_default_values(client, test_user_model):
    login_json = {
        "username": "calvarez",
        "password": "123456",
        "code": "12345678"
    }
    login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
    account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                   headers={'Authorization': login_response.json['access_token']})
    assert account_response.status_code == 200
    assert account_response.json['balance'] == 0.0
    assert account_response.json['currency'] == "local"
    cbu= 10200000000 + 2 * 10000 + 0 + 1    # 10200020001
    assert account_response.json['cbu'] == cbu


def test_associate_user_account(client, test_user_model):
    login_json = {
        "username": "calvarez",
        "password": "123456",
        "code": "12345678"
    }
    login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
    assert login_response.status_code == 200
    account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                   headers={'Authorization': login_response.json['access_token']})

    assert account_response.status_code == 200
    assert account_response.json['user_id'] == 2
