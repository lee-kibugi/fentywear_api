from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    # Import Blueprints
    from .routes.user_routes import user_bp
    from .routes.category_routes import category_bp
    from .routes.product_routes import product_bp
    from .routes.review_routes import review_bp

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(review_bp, url_prefix='/reviews')

    return app
