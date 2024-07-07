from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import config  # importing the different config classes (testing, production etc)

db = SQLAlchemy()  # db
migrate = Migrate()  # flask db
jwt = JWTManager()  # access_token

def create_app(config_name='production'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Importing here to avoid circular imports
    from .routes import main
    from .auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
