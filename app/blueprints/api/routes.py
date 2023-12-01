from flask import request
from . import api
from app import db
from app.models import User
from .auth import basic_auth, token_auth


@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user=basic_auth.current_user()
    token=auth_user.get_token()
    return {'token': token}

@api.route('/users', methods=['Post'])
def create_user():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    data=request.json

    required_fields=['username', 'password']
    missing_fields=[]
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    username=data.get('username')
    password=data.get('password')

    check_user=db.session.execute(db.select(User).where( (User.username==username))).scalars().all()
    if check_user:
        return {'error': 'A user with that username already exists'}
    
    new_user=User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict(), 201

@api.route('/users/me', methods=["GET"])
def get_me():
    current_user=token_auth.current_user()
    return current_user.to_dict()