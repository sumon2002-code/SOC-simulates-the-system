from os import getenv, urandom
from dotenv import load_dotenv

load_dotenv()

class Configs():
    # SERVER_NAME = getenv('SERVER_NAME')
    SERVER_NAME_MAIL = getenv('SERVER_NAME_MAIL')
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = '123as1df321sad32f1as32df132as1df'
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_PORT = getenv('MAIL_PORT')
    REDIS_SERVER_URL = getenv('REDIS_SERVER_URL')
