from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from app.models.category import Category
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity


# Create a new product
@jwt_required()
def create_product():
    data = request.get_json()

    required_fields = ['name', 'description', 'price', 'stock_quantity', 'image_url', 'category_id']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400

    try:
        product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock_quantity=data['stock_quantity'],
            image_url=data['image_url'],
            category_id=data['category_id'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get all products
def get_products():
    category_name = request.args.get('category')
    if category_name:
        products = Product.query.join(Category).filter(Category.name == category_name).all()
    else:
        products = Product.query.all()
    
    return jsonify([product.to_dict() for product in products]), 200

# Get a single product by ID
@jwt_required()
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200

# Update a product
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.category_id = data.get('category_id', product.category_id)
    product.image_url = data.get('image_url', product.image_url)
    db.session.commit()
    return jsonify(product.to_dict()), 200

# Delete a product
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock_quantity': product.stock_quantity,
        'category_id': product.category_id,
        'category_name': product.category.name if product.category else None,
        'image_url': product.image_url,
        'reviews': [review.to_dict() for review in product.reviews]
    }

Product.to_dict = product_to_dict
