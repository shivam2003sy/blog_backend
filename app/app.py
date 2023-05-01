import os 
from flask_cors import CORS 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mail import Mail
from celery import Celery
from flask_caching import Cache
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'app/static/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
CORS(app)
app.config.from_object('app.config.Config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
bc = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)
api = Api(app)
celery = None
celery = Celery(app)
mail =None
mail = Mail(app)
cache = None
cache = Cache(app)
celery.conf.update({
    'broker_url': app.config['CELERY_BROKER_URL'],
    'result_backend': app.config['CELERY_RESULT_BACKEND'],
})
celery.Task = celery.Task
jwt = JWTManager(app)
@app.before_first_request
def initialize_database():
    db.create_all()
from app import  models , views
