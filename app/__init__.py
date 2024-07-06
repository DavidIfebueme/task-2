from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
# from .models import *

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    #importing here just so i dont create a useless import loop that goes on forever and break my mf app
    from .routes import main
    from .auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app

