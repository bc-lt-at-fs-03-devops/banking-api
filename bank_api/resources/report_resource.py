from flask_restful import Resource
from flask import request, jsonify
import logging
from bank_api.models.transaction import Transaction
from bank_api.database import db
from sqlalchemy import and_, or_, not_, extract

REPORT_ENDPOINT = "/report_transactions"
logger = logging.getLogger(__name__)


class ReportResource(Resource):

    def get(self):
        year = request.get_json()["year"]
        month = request.get_json()["month"]
        cbu = request.get_json()["cbu"]

        transactions = Transaction.query.filter(
                or_(Transaction.origin_account == cbu,
                    Transaction.final_account == cbu)
                # and_(extract('month',Transaction.date) == month,
                #      extract('year', Transaction.date) == year)
        )
        transactions_arr = []
        for transaction in transactions:
            transaction_dict = transaction.__dict__
            transaction_dict.pop('_sa_instance_state')
            transactions_arr.append(transaction_dict)

        return jsonify(transactions=transactions_arr)
