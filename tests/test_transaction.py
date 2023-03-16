import datetime

from bank_api.resources.account_resource import ACCOUNT_ENDPOINT
from bank_api.resources.login_resource import LOGIN_ENDPOINT
from bank_api.resources.transaction_resource import TRANSACTION_ENDPOINT


def test_deposit(client, test_user_model):
    login_json = {
        "username": "calvarez",
        "password": "123456",
        "code": "12345678"
    }
    login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
    account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                   headers={'Authorization': login_response.json['access_token']})
    assert account_response.status_code == 200
    cbu = account_response.json['cbu']
    transaction_json = {
        "transaction_type": "deposit",
        "origin_account": 423424,
        "final_account": cbu,
        "description": "test deposit",
        "amount": 100.0
    }
    transaction_response = client.post(f"{TRANSACTION_ENDPOINT}", json=transaction_json)
    assert transaction_response.status_code == 200
    print(account_response.json)
    assert transaction_response.json['balance'] == 100.0

# for DEMO
# def test_deposit_negative_amount(client, test_user_model):
#     login_json = {
#         "username": "calvarez",
#         "password": "123456",
#         "code": "12345678"
#     }
#     login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
#     account_response = client.post(f"{ACCOUNT_ENDPOINT}",
#                                    headers={'Authorization': login_response.json['access_token']})
#     assert account_response.status_code == 200
#     cbu = account_response.json['cbu']
#     transaction_json = {
#         "transaction_type": "deposit",
#         "origin_account": 423424,
#         "final_account": cbu,
#         "description": "test deposit",
#         "amount": -100.0
#     }
#     transaction_response = client.post(f"{TRANSACTION_ENDPOINT}", json=transaction_json)
#     assert transaction_response.status_code == 404


def test_withdraw(client, test_user_model):
        test_deposit(client, test_user_model)
        login_json = {
            "username": "calvarez",
            "password": "123456",
            "code": "12345678"
        }
        login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
        account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                       headers={'Authorization': login_response.json['access_token']})
        assert account_response.status_code == 200
        cbu = account_response.json['cbu']
        transaction_json = {
                "transaction_type": "withdraw",
                "origin_account": cbu,
                "final_account": 13443523,
                "description": "test deposit",
                "amount": 10.0
            }
        transaction_response = client.post(f"{TRANSACTION_ENDPOINT}", json=transaction_json)
        assert transaction_response.status_code == 200
        assert transaction_response.json['balance'] == 90.0

def test_withdraw_amount_bigger_origin(client, test_user_model):
        test_deposit(client, test_user_model)
        login_json = {
            "username": "calvarez",
            "password": "123456",
            "code": "12345678"
        }
        login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
        account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                       headers={'Authorization': login_response.json['access_token']})
        assert account_response.status_code == 200
        cbu = account_response.json['cbu']
        transaction_json = {
                "transaction_type": "withdraw",
                "origin_account": cbu,
                "final_account": 13443523,
                "description": "test deposit",
                "amount": 10000.0
            }
        transaction_response = client.post(f"{TRANSACTION_ENDPOINT}", json=transaction_json)
        assert transaction_response.status_code == 404

def test_transaction(client, test_user_model):
        test_deposit(client, test_user_model)
        login_json = {
            "username": "calvarez",
            "password": "123456",
            "code": "12345678"
        }
        login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
        account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                       headers={'Authorization': login_response.json['access_token']})
        assert account_response.status_code == 200
        cbu_origin = account_response.json['cbu']
        account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                       headers={'Authorization': login_response.json['access_token']})
        assert account_response.status_code == 200
        cbu_destiny = account_response.json['cbu']
        transaction_json = {
                "transaction_type": "transaction",
                "origin_account": cbu_origin,
                "final_account": cbu_destiny,
                "description": "test transaction",
                "amount": 10.0
            }
        transaction_response = client.post(f"{TRANSACTION_ENDPOINT}", json=transaction_json)
        assert transaction_response.status_code == 200
        assert transaction_response.json['balance'] == account_response.json['balance'] + transaction_response.json['amount']
        assert transaction_response.json['final_account'] == cbu_destiny

# for PREDEMO
def test_transaction_amount_bigger_balance(client, test_user_model):
        test_deposit(client, test_user_model)
        login_json = {
            "username": "calvarez",
            "password": "123456",
            "code": "12345678"
        }
        login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
        account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                       headers={'Authorization': login_response.json['access_token']})
        assert account_response.status_code == 200
        cbu_origin = account_response.json['cbu']
        account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                       headers={'Authorization': login_response.json['access_token']})
        assert account_response.status_code == 200
        cbu_destiny = account_response.json['cbu']
        transaction_json = {
                "transaction_type": "transaction",
                "origin_account": cbu_origin,
                "final_account": cbu_destiny,
                "description": "test transaction",
                "amount": 100000.0
            }
        transaction_response = client.post(f"{TRANSACTION_ENDPOINT}", json=transaction_json)
        assert transaction_response.status_code == 404

# for DEMO
def test_transaction_negative_amount(client, test_user_model):
        test_deposit(client, test_user_model)
        login_json = {
            "username": "calvarez",
            "password": "123456",
            "code": "12345678"
        }
        login_response = client.post(f"{LOGIN_ENDPOINT}", json=login_json)
        account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                       headers={'Authorization': login_response.json['access_token']})
        assert account_response.status_code == 200
        cbu_origin = account_response.json['cbu']
        account_response = client.post(f"{ACCOUNT_ENDPOINT}",
                                       headers={'Authorization': login_response.json['access_token']})
        assert account_response.status_code == 200
        cbu_destiny = account_response.json['cbu']
        transaction_json = {
                "transaction_type": "transaction",
                "origin_account": cbu_origin,
                "final_account": cbu_destiny,
                "description": "test transaction",
                "amount": -100.0
            }
        transaction_response = client.post(f"{TRANSACTION_ENDPOINT}", json=transaction_json)
        assert transaction_response.status_code == 400