import os
from   decouple import config
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    CSRF_ENABLED = True
    SECRET_KEY = config('SECRET_KEY', default='abcdefghijklmnopqrst')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bloglite.sqlite3')
    SQLALCHEMY_DATABASE_URI = 'postgresql://wtghexqb:lrBw78aFPZhdvW6imWpQqgVcMOh-wbZV@arjuna.db.elephantsql.com/wtghexqb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'yourname@outlook.com'
    MAIL_PASSWORD = 'yourownpassword'
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = '3'

