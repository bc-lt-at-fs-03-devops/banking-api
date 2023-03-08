from marshmallow import Schema, fields, post_load
from bank_api.models.transaction import Transaction


class TransactionSchema(Schema):
    id = fields.Int(allow_none=False)
    transaction_type = fields.Str(allow_none=False)
    origin_account = fields.Integer(allow_none=False)
    final_account = fields.Integer(allow_none=False)
    description = fields.Str(allow_none=False)
    amount = fields.Float(allow_none=False)
    date = fields.Date(allow_none=False)

    @post_load
    def make_account(self, data, **kwargs):
        return Transaction(**data)
