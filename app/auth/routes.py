from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models import User, Organisation, UserOrganisation
import uuid

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user_id = data.get('userId')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    if not all([user_id, first_name, last_name, email, password]):
        return jsonify({"errors": [{"field": "input", "message": "All fields are required"}]}), 422

    if User.query.filter_by(email=email).first():
        return jsonify({"errors": [{"field": "email", "message": "Email already in use"}]}), 422

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

    access_token = create_access_token(identity=user_id)
    return jsonify({"status": "success", "message": "Registration successful", "data": {"accessToken": access_token, "user": {"userId": user_id, "firstName": first_name, "lastName": last_name, "email": email, "phone": phone}}}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"status": "Bad request", "message": "Authentication failed", "statusCode": 401}), 401

    access_token = create_access_token(identity=user.user_id)
    return jsonify({"status": "success", "message": "Login successful", "data": {"accessToken": access_token, "user": {"userId": user.user_id, "firstName": user.first_name, "lastName": user.last_name, "email": user.email, "phone": user.phone}}}), 200
