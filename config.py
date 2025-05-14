import os
from datetime import timedelta, datetime

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_JOIN_USER_ROLES = True
    SECURITY_TRACKABLE = True
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

    # SECURITY_TOKEN_MAX_AGE = datetime.now() + timedelta(days=100)
    # SECURITY_TOKEN_EXPIRE_TIMESTAMP = lambda user: 0
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    SECURITY_TOKEN_MAX_AGE = datetime.now() + timedelta(days=100)
    
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 120
    CACHE_REDIS_DB = 0
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'no-reply@Pustakalay.com'
    
    # broker_url = 'redis://localhost:6379/1'
    # result_backend = 'redis://localhost:6379/2'
    

