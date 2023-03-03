import datetime
from sqlalchemy import select
from bank_api.database import db
from sqlalchemy import text


def generate_cbu(context):
    user_id = context.get_current_parameters()['user_id']
    accounts = select(Account).where(Account.user_id == user_id)
    query = text(f"SELECT count(*) AS count FROM Account WHERE user_id like '{user_id}%'")
    count = db.session.scalars(query).first()
    print(count)
    cbu = 10200000000 + user_id * 10000 + count + 1
    return cbu


class Account(db.Model):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer())
    cbu = db.Column(db.Integer(), default=generate_cbu)
    balance = db.Column(db.Float(), default=0.0)
    currency = db.Column(db.String(), default="local")
    creation_date = db.Column(db.Date(), default=datetime.date.today())
