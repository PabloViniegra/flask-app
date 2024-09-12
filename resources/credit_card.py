from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.credit_card import CreditCardModel
from schemas.schemas import CreditCardSchema, PlainCreditCardSchema, UpdateCreditCardSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
import bcrypt

blp = Blueprint('credit_cards', __name__, description = 'Operation on credit cards')

@blp.route('/credit_cards')
class CreditCardList(MethodView):
    @blp.response(200, CreditCardSchema(many=True))
    @blp.response(500, description="Internal Server Error.")
    def get(self):
        try:
            credit_cards = CreditCardModel.query.all()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while retrieving addresses"
            )
        credit_card_schema = CreditCardSchema(many=True)
        serialized_credit_cards = credit_card_schema.dump(credit_cards)
        return serialized_credit_cards, 200
    @blp.response(201, CreditCardSchema)
    @blp.response(400, description="Credit Card already exists in database")
    @blp.response(500, description="Internal Server Error.")
    @blp.arguments(PlainCreditCardSchema)
    def post(self, credit_card_data):
        
        credit_card = CreditCardModel(**credit_card_data)
        salt = bcrypt.gensalt()
        credit_card.cvv = bcrypt.hashpw(credit_card.cvv.encode('utf-8'), salt)
        try:
            db.session.add(credit_card)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while inserting a credit card"
            )
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            abort(
                400,
                message="credit card already exists"
            )
            
        return CreditCardSchema().dump(credit_card), 201
    
@blp.route('/credit_cards/<int:credit_card_id>')
class CreditCard(MethodView):
    @blp.response(200, CreditCardSchema)
    @blp.response(404, description="Credit card indicated was not found in database")
    @blp.response(500, description="Internal Server Error.")
    def get(self, credit_card_id):
        try:
            credit_card = CreditCardModel.query.get_or_404(credit_card_id)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while retrieving the credit card"
            )
        return CreditCardSchema().dump(credit_card), 200
    @blp.arguments(UpdateCreditCardSchema)
    @blp.response(200, CreditCardSchema)
    @blp.response(404, description="Credit card was not found")
    @blp.response(500, description="Internal Server Error") 
    def put(self, credit_card_data, credit_card_id):
        
        credit_card = CreditCardModel.query.get(credit_card_id)
        if not credit_card:
            abort(
                404,
                message=f"Credit card {credit_card_id} was not founded"
            )
        credit_card.fullname = credit_card_data.get('fullname', credit_card.fullname)
        credit_card.card_number = credit_card_data.get('card_number', credit_card.card_number)
        credit_card.expired = credit_card_data.get('expired', credit_card.expired)
        
        if 'cvv' in credit_card_data:
            salt = bcrypt.gensalt()
            credit_card.cvv = bcrypt.hashpw(credit_card_data['cvv'].encode('utf-8'), salt)
        
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while updating the credit card"
            )
        return CreditCardSchema().dump(credit_card), 200
    @blp.response(204, description="Credit card succesfully deleted")
    @blp.response(404, description="Credit card indicated was not found in database")
    @blp.response(500, description="Internal Server Error.")
    def delete(self, credit_card_id):
        credit_card = CreditCardModel.query.get(credit_card_id)
        if not credit_card:
            abort(
                404,
                message=f"Credit card {credit_card_id} not founded"
            )
        try:
            db.session.delete(credit_card)
            db.session.commit()
            
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error has occurred while deleting the credit card"
            )
        return '', 204