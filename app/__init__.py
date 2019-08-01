from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bae.db'
heroku = Heroku(app)
db.init_app(app)
    
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
    
from .models import User, Writing
    
@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))
    
        #blueprint for routes that require auth 
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
    
        # blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

""" 
so the objects of this app
User
Prompt Session
Writing

User + User meet in a Prompt Session and create Writings which are sent to each other
"""


