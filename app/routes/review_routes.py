from flask import Blueprint, request, jsonify
from app import db
from app.models.review import Review
from flask_jwt_extended import jwt_required, get_jwt_identity

review_bp = Blueprint('review_bp', __name__)

# Create a new review
@review_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()

    try:
        review = Review(
            user_id=data['user_id'],
            product_id=data['product_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        db.session.add(review)
        db.session.commit()
        return jsonify(review.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get all reviews for a product
@review_bp.route('/product/<int:product_id>', methods=['GET'])
@jwt_required()
def get_reviews_for_product(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

# Get a single review
@review_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_review(id):
    review = Review.query.get_or_404(id)
    return jsonify(review.to_dict()), 200

# Update a review
@review_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id):
    review = Review.query.get_or_404(id)
    data = request.get_json()
    review.product_id = data.get('product_id', review.product_id)
    review.rating = data.get('rating', review.rating)
    review.comment = data.get('comment', review.comment)
    db.session.commit()
    return jsonify(review.to_dict()), 200

# Delete a review
@review_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'}), 200

def review_to_dict(review):
    return {
        'id': review.id,
        'product_id': review.product_id,
        'user_id': review.user_id,
        'rating': review.rating,
        'comment': review.comment,
    }

Review.to_dict = review_to_dict
