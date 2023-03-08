from flask_restful import Resource
from flask import jsonify
from bank_api.models.account import Account
from bank_api.models.user import User
from bank_api.database import db

ACCOUNT_INFO_ENDPOINT="/accounts/<int:cbu>"

class AccountInfoResource(Resource):

    def get(self, cbu):

        account = db.one_or_404(
            db.select(Account).filter_by(cbu = cbu),
            description=f"CBU {cbu} not found")
        
        user = db.session.execute(db.select(User).filter_by(id=account.user_id)).scalar_one()

        return jsonify(
                    cbu = account.cbu,
                    creation_date = account.creation_date,
                    username = user.username,
                    first_name=user.first_name,
                    last_name=user.last_name )
