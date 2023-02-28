from shutil import copy
from bank_api.api import create_app
from bank_api.constants import BANK_DATABASE, PROJECT_ROOT
import pytest
from bank_api.database import db
from bank_api.models.user import User
import datetime

@pytest.fixture()
def app(tmpdir):

    copy(f"{PROJECT_ROOT}/{BANK_DATABASE}", tmpdir.dirpath())
    temp_db_file = f"sqlite:///{tmpdir.dirpath()}/{BANK_DATABASE}"
    app = create_app(temp_db_file)
    app.config["TESTING"] = True

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def test_user_model(app):
    user1 = User( 
        first_name = "carlos",
        last_name = "alvarez",
        type = "client",
        birthday = datetime.datetime(1997, 1, 1),
        document_id = "123443221",
        country = "peru",
        city = "lima",
        address = "av siempreviva 123",
        email = "johndoe@testing.com",
        phone_number = "999555999",
        username = "calvarez",
        password = "123456",
        code = "12345678"
        )

    with app.app_context():
        db.session.add(user1)
        db.session.commit()
