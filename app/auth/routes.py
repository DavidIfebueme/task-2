from flask import Blueprint, request, jsonify, Response, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token #this is my first time using access_tokens walai
from app import db
from app.models import User, Organisation, UserOrganisation
import uuid #for random user and  org id

auth = Blueprint('auth', __name__) #auth/

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    errors = []
    # this is very ugly code but it is what it is
    if not first_name:
        errors.append({"field": "firstName", "message": "First name is required"})
    if not last_name:
        errors.append({"field": "lastName", "message": "Last name is required"})
    if not email:
        errors.append({"field": "email", "message": "Email is required"})
    if not password:
        errors.append({"field": "password", "message": "Password is required"})
    
    # i am honestly embarrassed by the rubbish i just wrote
    if errors:
        return jsonify({"errors": errors}), 422

    if User.query.filter_by(email=email).first():
        return jsonify({"errors": [{"field": "email", "message": "Email already in use"}]}), 422

    user_id = str(uuid.uuid4()) #im such a fool walai

    #hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, email=email, password=password, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    org_id = str(uuid.uuid4()) # creating random unique id
    org_name = f"{first_name}'s Organisation"
    new_org = Organisation(org_id=org_id, name=org_name)
    #should probably have a description here. edit: description is nullable so not required
    db.session.add(new_org)
    db.session.commit()

    user_org = UserOrganisation(user_id=user_id, org_id=org_id)
    db.session.add(user_org)
    db.session.commit()

    access_token = create_access_token(identity=user_id) #question: how long do access tokens even last
     response_data = {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": {
                "userId": user_id,
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "phone": phone
            }
        }
    }
    
    response = Response(json.dumps(response_data, sort_keys=False), mimetype='application/json')
    return response, 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first() #must be unique email. come to think of it i wonder if there should be regex for these fields

    if not user or not user.check_password(password):
        return jsonify({"status": "Bad request", "message": "Authentication failed", "statusCode": 401}), 401

    access_token = create_access_token(identity=user.user_id)
    return jsonify({"status": "success", "message": "Login successful", "data": {"accessToken": access_token, "user": {"userId": user.user_id, "firstName": user.first_name, "lastName": user.last_name, "email": user.email, "phone": user.phone}}}), 200
