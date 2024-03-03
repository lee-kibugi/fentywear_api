from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

from .routes.authentication import login, logout
from .routes.review_routes import create_review, get_reviews_for_product, get_review, update_review, delete_review
from .routes.user_routes import create_user, get_users, get_user, update_user, delete_user
from .routes.product_routes import create_product, get_products, get_product, update_product, delete_product
from .routes.category_routes import create_category, get_categories, get_category, update_category, delete_category

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt = JWTManager(app)

    app.add_url_rule('/api/auth/login', view_func=login, methods=['POST'])
    app.add_url_rule('/api/auth/logout', view_func=logout, methods=['POST'])

    app.add_url_rule('/api/users', view_func=create_user, methods=['POST'])
    app.add_url_rule('/api/users', view_func=get_users, methods=['GET'])
    app.add_url_rule('/api/users/<int:user_id>', view_func=get_user, methods=['GET'])
    app.add_url_rule('/api/users/<int:user_id>', view_func=update_user, methods=['PUT'])
    app.add_url_rule('/users/<int:user_id>', view_func=delete_user, methods=['DELETE'])

    app.add_url_rule('/api/categories', view_func=create_category, methods=['POST'])
    app.add_url_rule('/api/categories', view_func=get_categories, methods=['GET'])
    app.add_url_rule('/api/categories/<int:id>', view_func=get_category, methods=['GET'])
    app.add_url_rule('/api/categories/<int:id>', view_func=update_category, methods=['PUT'])
    app.add_url_rule('/api/categories/<int:id>', view_func=delete_category, methods=['DELETE'])

    app.add_url_rule('/api/products', view_func=create_product, methods=['POST'])
    app.add_url_rule('/api/products', view_func=get_products, methods=['GET'])
    app.add_url_rule('/api/products/<int:id>', view_func=get_product, methods=['GET'])
    app.add_url_rule('/api/products/<int:id>', view_func=update_product, methods=['PUT'])
    app.add_url_rule('/api/products/<int:id>', view_func=delete_product, methods=['DELETE'])

    app.add_url_rule('/api/reviews', view_func=create_review, methods=['POST'])
    app.add_url_rule('/api/reviews/product/<int:product_id>', view_func=get_reviews_for_product, methods=['GET'])
    app.add_url_rule('/api/reviews/<int:id>', view_func=get_review, methods=['GET'])
    app.add_url_rule('/api/reviews/<int:id>', view_func=update_review, methods=['PUT'])
    app.add_url_rule('/api/reviews/<int:id>', view_func=delete_review, methods=['DELETE'])

    return app
