from db import db

class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    addresses = db.relationship("AddressModel", back_populates="user", lazy="dynamic")
    credit_cards = db.relationship("CreditCardModel", back_populates="user", lazy="dynamic")