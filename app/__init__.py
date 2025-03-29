from flask import Flask
from flask_jwt_extended import JWTManager
from redis_config import ACCESS_EXPIRES
from sql_alchemy import database

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

    database.init_app(app)
    jwt = JWTManager(app)

    from .utils import check_if_token_is_revoked
    jwt.token_in_blocklist_loader(check_if_token_is_revoked)

    return app
