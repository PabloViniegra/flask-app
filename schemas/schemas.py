from marshmallow import Schema, fields
from models.user import UserModel
from models.address import AddressModel
from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemyAutoSchema

class PlainUserSchema(Schema):
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Str(required=True)
    date = fields.DateTime(required=True)
    password = fields.Str(required=True, load_only=True)

class PlainAddressSchema(Schema):
    street = fields.Str(required=True)
    number = fields.Int(required=False)
    stair = fields.Int(required=False)
    portal = fields.Int(required=False)
    door = fields.Int(required=True)
    letter = fields.Str(required=True)
    postal_code = fields.Int(required=True)
    city = fields.Str(required=True)
    province = fields.Str(required=True)
    user_id = fields.Int(required=True, load_only=True)
    
class PlainCreditCardSchema(Schema):
    fullname = fields.Str(required=False)
    card_number = fields.Str(required=True)
    expired = fields.Str(required=True)
    cvv = fields.Str(required=True, load_only=True)
    user_id = fields.Int(required=True, load_only=True)
    
class UserSchema(PlainUserSchema):
    id = fields.Str(dump_only=True)
    addresses = fields.List(fields.Nested(PlainAddressSchema()), dump_only=True)
    credit_cards = fields.List(fields.Nested(PlainCreditCardSchema()), dump_only=True)
    
class AddressSchema(PlainAddressSchema):
    id = fields.Str(dump_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    
    
class CreditCardSchema(PlainCreditCardSchema):
    id = fields.Str(dump_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)


#UPDATE SCHEMAS

class UpdateUserSchema(Schema):
    name = fields.Str(required=False)
    lastname = fields.Str(required=False)
    email = fields.Str(required=False)
    date = fields.DateTime(required=False)
    password = fields.Str(required=False)
    
class UpdateAddressSchema(Schema):
    street = fields.Str(required=False)
    number = fields.Int(required=False)
    stair = fields.Int(required=False)
    portal = fields.Int(required=False)
    door = fields.Int(required=False)
    letter = fields.Str(required=False)
    postal_code = fields.Int(required=False)
    city = fields.Str(required=False)
    province = fields.Str(required=False)
    
class UpdateCreditCardSchema(Schema):
    fullname = fields.Str(required=False)
    card_number = fields.Str(required=False)
    expired = fields.Str(required=False)
    cvv = fields.Str(required=False)