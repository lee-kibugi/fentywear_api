from flask import Flask
from .user_routes import user_bp
from .category_routes import category_bp
from .product_routes import product_bp
from .review_routes import review_bp
from .authentication import auth_bp

def register_blueprints(app: Flask):
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(review_bp, url_prefix='/reviews')
    app.register_blueprint(auth_bp, url_prefix='/auth')
