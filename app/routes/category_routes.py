from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    existing_category = Category.query.filter_by(name=data['name']).first()
    
    if existing_category:
        return jsonify({'error': 'Category with this name already exists'}), 400

    new_category = Category(
        name=data['name'],
        description=data['description'],
        image_url=data.get('image_url', '')
    )
    db.session.add(new_category)
    try:
        db.session.commit()
        return jsonify(new_category.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


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
    category.image_url = data.get('image_url', category.image_url) 
    db.session.commit()
    return jsonify(category.to_dict()), 200

# Delete a category
@category_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'}), 200

def category_to_dict(category):
    return {
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'image_url': category.image_url,
        "products": [product.to_dict() for product in category.products]
    }

Category.to_dict = category_to_dict
