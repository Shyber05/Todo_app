from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'     
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)    
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from todo import routes
