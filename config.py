import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #no dey try find my secret keys jooor
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') #usually i should have a seperate db for tests but c'mon...

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config): #probably not gonna need this for this projet but still stay here cause ill need to reference this repo in the future. turns out i needed it
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': Config
}    