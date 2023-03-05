import logging
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort
from marshmallow import ValidationError
from sqlalchemy import select
from bank_api.database import db
from bank_api.models.user import User
from bank_api.schemas.account_schema import AccountSchema
from bank_api.models.account import Account

ACCOUNT_ENDPOINT = "/accounts"
logger = logging.getLogger(__name__)


class AccountResource(Resource):

    @jwt_required()
    def post(self):
        try:
            username = get_jwt_identity()
            user = db.one_or_404(
                db.select(User).filter_by(username=username),
                description=f"No user named '{username}'")
            user_dict = user.__dict__
            user_id = user_dict['id']
            account = AccountSchema().load({"user_id": user_id})
            db.session.add(account)
            db.session.commit()

            account = db.one_or_404(
                db.select(Account).filter_by(user_id=user_id),
                description=f"No account for user '{user_id}'")
            account_dict = account.__dict__
            account_dict.pop("_sa_instance_state")
            print(account_dict)
            logger.debug(f"Create new account by {user.username}")
            return jsonify(account_dict)

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
        account = db.one_or_404(
            db.select(Account).filter_by(user_id=user_id),
            description=f"No account for user '{user_id}'")
        account_dict = account.__dict__
        account_dict.pop("_sa_instance_state")
        print(account_dict)
        return jsonify(account_dict)
