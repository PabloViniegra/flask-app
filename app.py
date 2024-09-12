from flask import Flask
from flask_smorest import Api
from resources.user import blp as UserBlueprint
from resources.address import blp as AddressBlueprint
from resources.credit_card import blp as CreditCardBlueprint
from flask_marshmallow import Marshmallow
from db import db
import models
import os


def create_app(db_url = None):
    app = Flask(__name__)

    # CONFIGURATIONS
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'Client REST API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    @app.before_request
    def create_tables():
        db.create_all()
    
    api = Api(app)
    ma = Marshmallow(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(AddressBlueprint)
    api.register_blueprint(CreditCardBlueprint)
    return app