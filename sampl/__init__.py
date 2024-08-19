import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sampl_database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['CACHE_TYPE'] = 'simple' # Later to adopt the redis caching tech
cache = Cache(app)
timeout = 3600

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'wassimhaimoudi1@gmail.com'
app.config['MAIL_PASSWORD'] = '24142424@Yassin'

mail = Mail(app)

from sampl import routes
