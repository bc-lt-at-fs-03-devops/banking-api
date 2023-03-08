import logging
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort
from marshmallow import ValidationError
from bank_api.database import db
from bank_api.models.user import User
from bank_api.schemas.account_schema import AccountSchema
from bank_api.models.account import Account

ACCOUNT_ENDPOINT = "/accounts"
logger = logging.getLogger(__name__)


def get_user_by_username(value):
    user = db.one_or_404(
        db.select(User).filter_by(username=value),
        description=f"No user with username '{value}'")
    if user:
        user = user.__dict__
        user.pop('_sa_instance_state')
        return user
    if not user:
        return value


def get_account(value):
    account = Account.query.filter_by(user_id=value).first()
    if account:
        return account
    if not account:
        return value


class AccountResource(Resource):
    @jwt_required()
    def post(self):
        try:
            username = get_jwt_identity()
            user = get_user_by_username(username)
            user_id = user['id']
            account = AccountSchema().load({"user_id": user_id})
            db.session.add(account)
            db.session.commit()
            account = get_account(user_id)
            logger.debug(f"Create new account by {username}")
            return jsonify(
                user_id=account.user_id,
                cbu=account.cbu,
                balance=account.balance,
                currency=account.currency,
                creation_date=account.creation_date)

        except ValidationError as e:
            logger.warning(f"Validation error:  {e.messages} ")
            abort(405, errors=e.messages)

    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = db.one_or_404(
            db.select(User).filter_by(username=username),
            description=f"No user named '{username}'")
        user_dict = user.__dict__
        user_id = user_dict['id']
        accounts = db.one_or_404(
            db.select(Account).filter_by(user_id=user_id).all(),
            description=f"No account for user '{user_id}'")
        account_dict = accounts.__dict__
        account_dict.pop("_sa_instance_state")
        return jsonify(account_dict)
