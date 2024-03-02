from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'], description=data['description'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

# Get all categories
@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

# Get a single category by ID
@category_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict()), 200

# Update a category
@category_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    db.session.commit()
    return jsonify(category.to_dict()), 200

# Delete a category
@category_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'}), 200

# Assuming you have a to_dict method in your Category model for serialization
# If not, you'll need to implement it, like so:
def category_to_dict(category):
    return {
        'id': category.id,
        'name': category.name,
        'description': category.description
    }

# Dynamically add the serialization method to Category class
Category.to_dict = category_to_dict
