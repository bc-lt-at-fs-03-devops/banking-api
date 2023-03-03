import logging
from flask import jsonify
from bank_api.database import db
from bank_api.models.user import User
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

HOME_ENDPOINT = "/home"
logger = logging.getLogger(__name__)

class HomeResource(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = db.one_or_404(
            db.select(User).filter_by(username = username),
            description=f"No user named '{username}'")
        user_dict = user.__dict__
        user_dict.pop('_sa_instance_state')
        user_dict.pop('id')
        user_dict.pop('password')
        user_dict.pop('code')
        user_dict['birthday'] = user_dict['birthday'].strftime("%Y-%m-%d")
        #print(user_dict)
        return jsonify(user_dict)
