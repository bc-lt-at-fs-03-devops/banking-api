from bank_api.resources.login_resource import LOGIN_ENDPOINT
from bank_api.resources.users_resource import USERS_ENDPOINT
from bank_api.resources.home_resource import HOME_ENDPOINT

def test_home(client):
    # Create a example of user
    user_json = {
            "first_name": "jhon",
            "last_name": "doe",
            "type": "user",
            "document_id": "12345678",
            "birthday": "1997-01-01",
            "country": "peru",
            "city": "lima",
            "address": "av siempreviva",
            "email": "ca@texample.com",
            "phone_number": "999555999"
    } 
    # User data to login
    user_creation_response = client.post(f"{USERS_ENDPOINT}",json=user_json)
    print(user_creation_response.json)
    login_json = {
        "username": user_creation_response.json["username"],
        "password": user_creation_response.json["password"],
        "code": user_creation_response.json["code"] # The type of the "code" is a string and its is supposed to be integer
    }
    print(login_json)
    login_response = client.post(f"{LOGIN_ENDPOINT}",
                                 json=login_json)
    
    print(login_response.text)
    home_response = client.get(f'{HOME_ENDPOINT}',  
                               headers={'Authorization':login_response.json['access_token']})
    print(home_response.status_code)
    for key in user_json.keys():
        assert user_json[key] == home_response.json[key]
