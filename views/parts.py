from flask import Blueprint, request, jsonify
from models import db, Part, User
from flask_jwt_extended import jwt_required, get_jwt_identity

parts_bp = Blueprint('parts_bp', __name__)

# Function to check if the user is an admin
def check_if_admin():
    user_id = get_jwt_identity()  # Get user id from the JWT token
    user = User.query.get(user_id)  # Fetch the user from the database
    if user and user.is_admin:
        return True
    return False

# Add a new part (Only Admin)
@parts_bp.route("/part", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated
def add_part():
    if not check_if_admin():
        return jsonify({'msg': 'You are not authorized to perform this action'}), 403

    data = request.get_json()
    name = data['name']
    quantity = data['quantity']
    price = data['price']

    # Create a new part entry
    new_part = Part(name=name, quantity=quantity, price=price)
    db.session.add(new_part)
    db.session.commit()

    return jsonify({'msg': 'Part added successfully'}), 201

# Fetch all parts (Admin and non-admins can view)
@parts_bp.route("/parts", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated
def get_parts():
    parts = Part.query.all()
    output = []
    for part in parts:
        output.append({
            'id': part.id,
            'name': part.name,
            'quantity': part.quantity,
            'price': part.price
        })
    return jsonify(output), 200

# Fetch a single part by ID (Admin and non-admins can view)
@parts_bp.route("/parts/<int:part_id>", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated
def get_part(part_id):
    part = Part.query.get(part_id)
    if part:
        return jsonify({
            'id': part.id,
            'name': part.name,
            'quantity': part.quantity,
            'price': part.price
        }), 200
    else:
        return jsonify({'msg': 'Part not found'}), 404

# Update a part (Only Admin)
@parts_bp.route("/parts/<int:part_id>", methods=["PUT"])
@jwt_required()  # Ensure the user is authenticated
def update_part(part_id):
    if not check_if_admin():
        return jsonify({'msg': 'You are not authorized to perform this action'}), 403

    data = request.get_json()
    part = Part.query.get(part_id)

    if part:
        part.name = data.get('name', part.name)
        part.quantity = data.get('quantity', part.quantity)
        part.price = data.get('price', part.price)
        
        db.session.commit()
        return jsonify({'msg': 'Part updated successfully'}), 200
    else:
        return jsonify({'msg': 'Part not found'}), 404

# Delete a part (Only Admin)
@parts_bp.route("/parts/<int:part_id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated
def delete_part(part_id):
    if not check_if_admin():
        return jsonify({'msg': 'You are not authorized to perform this action'}), 403

    part = Part.query.get(part_id)
    if part:
        db.session.delete(part)
        db.session.commit()
        return jsonify({'msg': 'Part deleted successfully'}), 200
    else:
        return jsonify({'msg': 'Part not found'}), 404
