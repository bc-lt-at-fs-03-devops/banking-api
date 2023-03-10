from bank_api.api import create_app
from bank_api.constants import BANK_DATABASE
import pytest
from bank_api.database import db
from bank_api.models.user import User
import datetime
import tempfile

@pytest.fixture()
def app():
    temp_dir = tempfile.TemporaryDirectory()
    temp_db_file = f"sqlite:///{temp_dir.name}/{BANK_DATABASE}"
    app = create_app(temp_db_file)
    app.config["TESTING"] = True
    yield app
    temp_dir.cleanup()

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
