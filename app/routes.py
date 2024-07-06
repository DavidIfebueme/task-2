from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, Organisation, UserOrganisation
import uuid
from .models import db

main = Blueprint('main', __name__)

@main.route('/api/users/<string:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=id).first() #unique user id required

    if not user or user.user_id != current_user_id:
        return jsonify({"status": "error", "message": "User not found or unauthorized"}), 404

    return jsonify({"status": "success", "message": "User retrieved", "data": {"userId": user.user_id, "firstName": user.first_name, "lastName": user.last_name, "email": user.email, "phone": user.phone}}), 200


@main.route('/api/organisations', methods=['GET'])
@jwt_required()
def get_organisations():
    current_user_id = get_jwt_identity()
    user_orgs = UserOrganisation.query.filter_by(user_id=current_user_id).all()
    
    organisations = []
    for user_org in user_orgs:
        org = Organisation.query.filter_by(org_id=user_org.org_id).first()
        organisations.append({"orgId": org.org_id, "name": org.name, "description": org.description})
    
    return jsonify({"status": "success", "message": "Organisations retrieved", "data": {"organisations": organisations}}), 200

@main.route('/api/organisations/<string:orgId>', methods=['GET'])
@jwt_required()
def get_organisation(orgId):
    current_user_id = get_jwt_identity()
    user_org = UserOrganisation.query.filter_by(user_id=current_user_id, org_id=orgId).first()
    
    if not user_org:
        return jsonify({"status": "error", "message": "Organisation not found or unauthorized"}), 404
    
    org = Organisation.query.filter_by(org_id=orgId).first()
    return jsonify({"status": "success", "message": "Organisation retrieved", "data": {"orgId": org.org_id, "name": org.name, "description": org.description}}), 200

@main.route('/api/organisations', methods=['POST'])
@jwt_required()
def create_organisation():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description')
    
    if not name:
        return jsonify({"errors": [{"field": "name", "message": "Name is required"}]}), 422
    
    org_id = str(uuid.uuid4())
    new_org = Organisation(org_id=org_id, name=name, description=description)
    db.session.add(new_org)
    db.session.commit()
    
    user_org = UserOrganisation(user_id=current_user_id, org_id=org_id)
    db.session.add(user_org)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Organisation created successfully", "data": {"orgId": org_id, "name": name, "description": description}}), 201

@main.route('/api/organisations/<string:orgId>/users', methods=['POST'])
@jwt_required()
def add_user_to_organisation(orgId):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    user_id = data.get('userId')
    if not user_id:
        return jsonify({"errors": [{"field": "userId", "message": "User ID is required"}]}), 422
    
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"errors": [{"field": "userId", "message": "User not found"}]}), 404
    
    user_org = UserOrganisation.query.filter_by(user_id=user_id, org_id=orgId).first()
    if user_org:
        return jsonify({"errors": [{"field": "userId", "message": "User already in organisation"}]}), 422
    
    new_user_org = UserOrganisation(user_id=user_id, org_id=orgId)
    db.session.add(new_user_org)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "User added to organisation successfully"}), 200
