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

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt = JWTManager(app)

    # Import Blueprints
    from .routes.user_routes import user_bp
    from .routes.category_routes import category_bp
    from .routes.product_routes import product_bp
    from .routes.review_routes import review_bp
    from .routes.authentication import auth_bp

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(review_bp, url_prefix='/reviews')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
