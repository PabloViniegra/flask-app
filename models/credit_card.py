from db import db

class CreditCardModel(db.Model):
    __tablename__ = "credit_cards"
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable=True)
    card_number = db.Column(db.String(20), nullable=False)
    expired = db.Column(db.String(5), nullable= False)
    cvv = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        unique=False,
                        nullable=False)
    user = db.relationship("UserModel", back_populates="credit_cards", lazy="select")