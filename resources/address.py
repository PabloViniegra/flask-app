from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.address import AddressModel
from schemas.schemas import AddressSchema, PlainAddressSchema, UpdateAddressSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db


blp = Blueprint('addresses', __name__, description = 'Operation on addresses')


@blp.route('/address')
class AddressList(MethodView):
    @blp.response(200, AddressSchema(many=True))
    @blp.response(500, description="Internal Server Error.")
    def get(self):
        try:
            addresses = AddressModel.query.all()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while retrieving addresses"
            )
        address_schema = AddressSchema(many=True)
        serialized_addresses = address_schema.dump(addresses)
        return serialized_addresses, 200
    @blp.response(201, AddressSchema)
    @blp.response(400, description="address already exists.")
    @blp.response(500, description="Internal Server Error.")
    @blp.arguments(PlainAddressSchema)
    def post(self, address_data):
        address = AddressModel(**address_data)
        try:
            db.session.add(address)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while inserting an address"
            )
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            abort(
                400,
                message="address already exists"
            )
        
        serialized_address = AddressSchema().dump(address)  
        return serialized_address, 201

    
@blp.route('/address/<int:address_id>')
class Address(MethodView):
    @blp.response(200, AddressSchema)
    @blp.response(404, description="Address not found")
    @blp.response(500, description="Internal Server Error.")
    def get(self, address_id):
        try:
            address = AddressModel.query.get_or_404(address_id)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while retrieving the address"
            )
        return AddressSchema().dump(address), 200
    @blp.response(201, AddressSchema)
    @blp.response(404, description="Address not found")
    @blp.response(500, description="Internal Server Error")
    @blp.arguments(UpdateAddressSchema)
    def put(self, address_data, address_id):
        address = AddressModel.query.get(address_id)
        if not address:
            abort(
                404,
                message=f"address {address_id} was not found"
            )
        address.street = address_data.get('street', address.street)
        address.number = address_data.get('number', address.number)
        address.stair = address_data.get('stair', address.stair)
        address.street = address_data.get('street', address.street)
        address.portal = address_data.get('portal', address.portal)
        address.door = address_data.get('door', address.door)
        address.letter = address_data.get('letter', address.letter)
        address.postal_code = address_data.get('postal_code', address.postal_code)
        address.street = address_data.get('street', address.street)
        address.city = address_data.get('city', address.city)
        address.province = address_data.get('province', address.province)
        
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error occurred while updating an address"
            )
        return AddressSchema().dump(address), 201
    
    @blp.response(204, description="Address succesfully deleted")
    @blp.response(404, description="Address indicated was not found in database")
    @blp.response(500, description="Internal Server Error.")
    def delete(self, address_id):
        address = AddressModel.query.get(address_id)
        if not address:
            abort(
                404,
                message=f"address {address_id} not founded"
            )
        try:
            db.session.delete(address)
            db.session.commit()
            
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(
                500,
                message="An error has occurred while deleting the address"
            )
        return '', 204
        