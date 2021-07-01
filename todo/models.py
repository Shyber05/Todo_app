from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from todo import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=80), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_txt_password):
        self.password_hash = generate_password_hash(plain_txt_password)
       

    def check_password(self, password_attempt):
        return check_password_hash(self.password_hash, password_attempt)

    def __repr__(self):
        return f"{self.id}, {self.username}"

    
    

class ToDO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    due_date = db.Column(db.DateTime, default=datetime.utcnow())
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.id}>" 

