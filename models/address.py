from db import db

class AddressModel(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer(), nullable=True)
    stair = db.Column(db.Integer(), nullable=True)
    portal = db.Column(db.Integer(), nullable=True)
    door = db.Column(db.Integer(), nullable=False)
    letter = db.Column(db.String(5), nullable=False)
    postal_code = db.Column(db.Integer(), nullable=False)
    city = db.Column(db.String(60), nullable= False)
    province = db.Column(db.String(60), nullable= False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        unique=False,
                        nullable=False)
    user = db.relationship("UserModel", back_populates="addresses", lazy="select")
    