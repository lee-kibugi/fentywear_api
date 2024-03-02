from .. import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)
    image_url = db.Column(db.String(255), nullable=True)
