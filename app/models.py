from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import random
import base64
import os
from datetime import datetime, timedelta


class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, nullable=False, unique=True)
    password=db.Column(db.String, nullable=False)
    token=db.Column(db.String(32), index=True, unique=True)
    token_expiration=db.Column(db.DateTime)
    favorites=db.Column(db.Text, default='[]')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password=generate_password_hash(kwargs.get('password', ''))

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"
    
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
def get_token(self):
    now=datetime.utcnow()
    if self.token and self.token_expiration>now+timedelta(minutes=1):
        return self.token
    self.token=base64.b64encode(os.random(24)).decode('utf-8')
    self.token_expiration=now+timedelta(hours=1)
    db.session.commit()
    return self.token

@login.user_loader
def get_user(user_id):
    return db.session.get(User, user_id)



def to_dict(self):
    return {
        'id': self.id,
        'username': self.username,
        'password': self.password,
        'favorites': self.favorites
    }
