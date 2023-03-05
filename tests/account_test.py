from bank_api.resources.account_resource import ACCOUNT_ENDPOINT
from bank_api.resources.login_resource import LOGIN_ENDPOINT
from bank_api.resources.users_resource import USERS_ENDPOINT


def test_create_account(client):
    user_json = {
        "first_name": "jhon",
        "last_name": "doe",
        "type": "client-person",
        "document_id": "12345678",
        "birthday": "1997-01-01",
        "country": "peru",
        "city": "lima",
        "address": "av siempreviva",
        "email": "ca@texample.com",
        "phone_number": "999555999"
    }
    user_response = client.post(f"{USERS_ENDPOINT}", json=user_json)
    assert user_response.status_code == 201

    login_json = {
        "username": user_response.json["username"],
        "password": user_response.json["password"],
        "code": int(user_response.json["code"])
    }
    login_response = client.post(f"{LOGIN_ENDPOINT}",
                                 json=login_json)
    response = client.post(f"{ACCOUNT_ENDPOINT}",
                           headers={'Authorization': login_response.json['access_token']})
    assert user_response.json["id"] == response.json["user_id"]

