from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from models.credit_card import CreditCardModel
from models.user import UserModel
from schemas.schemas import CreditCardSchema, UserSchema, PlainUserSchema, UpdateUserSchema, PlainCreditCardSchema, PlainAddressSchema
from schemas.schemas import AddressSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import bcrypt
from flask import request

blp = Blueprint('users', __name__, description = 'Operation on users')

@blp.route('/users')
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @blp.response(500, description="Internal Server Error.")
    def get(self):
        search_text = request.args.get('text', None)
        try:
            if not search_text:
                users = UserModel.query.all()
            else:
                users = UserModel.query.filter(
                    or_(
                        UserModel.name.ilike(f'%{search_text}%'),
                        UserModel.lastname.ilike(f'%{search_text}%'),
                        UserModel.email.ilike(f'%{search_text}%')
                    )
                ).all()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while retrieving users"
            )
        user_schema = UserSchema(many=True)
        serialized_users = user_schema.dump(users)
        return serialized_users, 200
        
    @blp.response(201, UserSchema)
    @blp.response(400, description="User already exists in database")
    @blp.response(409, description="A user with that email already exists")
    @blp.response(500, description="Internal Server Error.")
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        
        if UserModel.query.filter(UserModel.email == user_data['email']).first():
            abort(
                409,
                message="A user with that email already exists"
            )
        user = UserModel(**user_data)
        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while inserting an user"
            )
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            abort(
                400,
                message="user already exists"
            )
            
        return UserSchema().dump(user), 201
    
@blp.route('/users/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    @blp.response(404, description="User indicated was not found in database")
    @blp.response(500, description="Internal Server Error.")
    def get(self, user_id):
        try:
            user = UserModel.query.get_or_404(user_id)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while retrieving the user"
            )
        return UserSchema().dump(user), 200
    @blp.response(200, UserSchema)
    @blp.response(404, description="User indicated was not found in database")
    @blp.response(409, description="A user with that email already exists")
    @blp.response(500, description="Internal Server Error.")
    @blp.arguments(UpdateUserSchema)
    def put(self, user_data, user_id):
        if UserModel.query.filter(UserModel.email == user_data['email']).first():
            abort(
                409,
                message="A user with that email already exists"
            )
        user = UserModel.query.get(user_id)
        if not user:
            abort(
                404,
                message=f"user {user_id} was not founded"
            )
        user.name = user_data.get('name', user.name)
        user.lastname = user_data.get('lastname', user.lastname)
        user.email = user_data.get('email', user.email)
        user.date = user_data.get('date', user.date)
        
        if 'password' in user_data:
            salt = bcrypt.gensalt()
            user.password = bcrypt.hashpw(user_data['password'].encode('utf-8'), salt)
        
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while updating the user"
            )
        return UserSchema().dump(user), 200
    @blp.response(204, description="User succesfully deleted")
    @blp.response(404, description="User indicated was not found in database")
    @blp.response(500, description="Internal Server Error.")
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(
                404,
                message=f"user {user_id} not founded"
            )
        try:
            db.session.delete(user)
            db.session.commit()
            
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error has occurred while deleting the user"
            )
        return '', 204
@blp.route('/users/<int:user_id>/addresses')
class UserToAddresses(MethodView):
    @blp.response(200, AddressSchema(many=True))
    @blp.response(404, description="User not found")
    @blp.response(500, description="Internal Server Error")
    def get(self, user_id):
        try:
            user = UserModel.query.get(user_id)
            if not user:
                abort(
                    404,
                    message="User was not found"
                )
            address_schema = AddressSchema(many=True)
            return address_schema.dump(user.addresses), 200    
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="Internal Server Error"
            )
            
@blp.route('/users/<int:user_id>/credit_cards')
class UserToCreditCards(MethodView):
    def get(self, user_id):
        try:
            user = UserModel.query.get(user_id)
            if not user:
                abort(
                    404,
                    message="User was not found"
                )
            credit_card_schema = CreditCardSchema(many=True)
            return credit_card_schema.dump(user.credit_cards), 200    
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="Internal Server Error"
            )
        