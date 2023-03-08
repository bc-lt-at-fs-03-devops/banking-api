import datetime
from sqlalchemy import select
from bank_api.database import db
from sqlalchemy import text


class Transaction(db.Model):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_type = db.Column(db.String)
    origin_account = db.Column(db.Integer)
    final_account = db.Column(db.Integer)
    amount = db.Column(db.Float)
    description = db.Column(db.String)
    date = db.Column(db.Date, default=datetime.date.today())
