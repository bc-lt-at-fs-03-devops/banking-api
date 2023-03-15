import logging
from flask import request, jsonify, make_response
from flask_restful import Resource, abort
from marshmallow import ValidationError
from bank_api.database import db
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
    return account


def save_transaction_to_db(transaction_dict):
    transaction = TransactionSchema().load(transaction_dict)
    db.session.add(transaction)
    db.session.commit()
    return transaction

def error_amount_negative():
    return make_response(jsonify(msg=f"The amount is negative"),404)

def deposit(transaction):
    if transaction['amount'] < 0:
        return error_amount_negative()
    cbu_destiny = transaction['final_account']
    final_account = get_account(cbu_destiny)
    destiny_balance = final_account['balance']
    new_balance = destiny_balance + transaction['amount']
    account = update_balance(cbu_destiny, new_balance)
    transaction = save_transaction_to_db(transaction)
    return jsonify(
        origin_account=transaction.origin_account,
        final_account=transaction.final_account,
        description=transaction.description,
        amount=transaction.amount,
        balance=account.balance)


def withdraw(transaction):
    if transaction['amount'] < 0:
        return error_amount_negative()
    cbu_origin = transaction['origin_account']
    origin_account = get_account(cbu_origin)
    origin_balance = origin_account['balance']
    if origin_balance < transaction['amount']:
        raise Exception("The amount to withdraw is bigger than current balance")
    new_balance = origin_balance - transaction['amount']
    account = update_balance(cbu_origin, new_balance)
    transaction = save_transaction_to_db(transaction)
    return jsonify(
        origin_account=transaction.origin_account,
        final_account=transaction.final_account,
        description=transaction.description,
        amount=transaction.amount,
        balance=account.balance)


def transaction(transaction):
    if transaction['amount'] < 0:
        return error_amount_negative()
    cbu_destiny = transaction['final_account']
    final_account = get_account(cbu_destiny)
    destiny_balance = final_account['balance']
    cbu_origin = transaction['origin_account']
    origin_account = get_account(cbu_origin)
    origin_balance = origin_account['balance']
    if origin_balance >= transaction['amount']:
        new_origin_balance = origin_balance - transaction['amount']
        account_origin = update_balance(cbu_origin, new_origin_balance)
        new_destiny_balance = destiny_balance + transaction['amount']
        account_final = update_balance(cbu_destiny, new_destiny_balance)
        transaction = save_transaction_to_db(transaction)
        return jsonify(
            origin_account=transaction.origin_account,
            final_account=transaction.final_account,
            description=transaction.description,
            amount=transaction.amount,
            balance=account_origin.balance)


class TransactionResource(Resource):
    def post(self):
        try:
            transaction_loaded = TransactionSchema().load(request.get_json())
            transaction_dict = transaction_loaded.__dict__
            transaction_dict.pop('_sa_instance_state')
            if transaction_dict['transaction_type'] == 'deposit':
                return deposit(transaction_dict)
            if transaction_dict['transaction_type'] == 'withdraw':
                return withdraw(transaction_dict)
            if transaction_dict['transaction_type'] == 'transaction':
                return transaction(transaction_dict)
        except ValidationError as e:
            logger.warning(f"Validation error:  {e.messages} ")
            abort(405, errors=e.messages)
