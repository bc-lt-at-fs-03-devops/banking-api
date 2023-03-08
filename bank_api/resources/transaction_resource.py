import logging
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort
from marshmallow import ValidationError
from sqlalchemy import select
from bank_api.database import db
from bank_api.models.user import User
from bank_api.schemas.transaction_schema import TransactionSchema
from bank_api.models.account import Account

TRANSACTION_ENDPOINT = "/transactions"
logger = logging.getLogger(__name__)


def get_account(cbu):
    account = db.one_or_404(
        db.select(Account).filter_by(cbu=cbu),
        description=f"No account with cbu '{cbu}'")
    if account:
        account = account.__dict__
        account.pop('_sa_instance_state')
        return account
    if not account:
        return cbu


def update_balance(cbu, new_balance):
    account = Account.query.filter_by(cbu=cbu).first()
    account.balance = new_balance
    db.session.commit()


def deposit(transaction):
    cbu_destiny = transaction['final_account']
    final_account = get_account(cbu_destiny)
    destiny_balance = final_account['balance']
    new_balance = destiny_balance + transaction['amount']
    update_balance(cbu_destiny, new_balance)


def withdraw(transaction):
    cbu_origin = transaction['origin_account']
    origin_account = get_account(cbu_origin)
    origin_balance = origin_account['balance']
    if origin_balance < transaction['amount']:
        raise Exception("The amount to withdraw is bigger than current balance")
    new_balance = origin_balance - transaction['amount']
    update_balance(cbu_origin, new_balance)


def transaction(transaction):
    cbu_destiny = transaction['final_account']
    final_account = get_account(cbu_destiny)
    destiny_balance = final_account['balance']
    cbu_origin = transaction['origin_account']
    origin_account = get_account(cbu_origin)
    origin_balance = origin_account['balance']
    if origin_balance >= transaction['amount']:
        new_origin_balance = origin_balance - transaction['amount']
        update_balance(cbu_origin, new_origin_balance)
        new_destiny_balance = destiny_balance + transaction['amount']
        update_balance(cbu_destiny, new_destiny_balance)


class TransactionResource(Resource):
    def post(self):
        try:
            transaction_loaded = TransactionSchema().load(request.get_json())
            transaction_dict = transaction_loaded.__dict__
            transaction_dict.pop('_sa_instance_state')
            if transaction_dict['transaction_type'] == 'deposit':
                deposit(transaction_dict)
            if transaction_dict['transaction_type'] == 'withdraw':
                withdraw(transaction_dict)
            if transaction_dict['transaction_type'] == 'transaction':
                transaction(transaction_dict)
        except ValidationError as e:
            logger.warning(f"Validation error:  {e.messages} ")
            abort(405, errors=e.messages)
