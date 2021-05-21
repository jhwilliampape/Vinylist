from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid   #unique user identifier - use for Primary Keys

#Adding Flask Security for password protection- built-in w/ Flask
from werkzeug.security import generate_password_hash, check_password_hash

#import Secrets module (provided by python)
import secrets

#import for flask-login classes
from flask_login import UserMixin, LoginManager

#Install Marshmallow
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    vinyl = db.relationship('Vinyl', backref = "owner", lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User: {self.email} has been created and added to the database"

class Vinyl(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    label = db.Column(db.String(100), nullable = True)
    format = db.Column(db.String(500), nullable = True)
    country = db.Column(db.String(100))
    released = db.Column(db.String(15))
    genre = db.Column(db.String(50))
    style = db.Column(db.String(100))
    price = db.Column(db.Numeric(precision = 10, scale = 2))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, label, format, country, released, genre, style, price, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.label = label
        self.format = format
        self.country = country
        self.released = released
        self.genre = genre
        self.style = style
        self.price = price
        self.user_token = user_token

    def __repr__(self):
        return f'The following Vinyl has been added: {self.name}'

    def set_id(self):
        return str(uuid.uuid4())


#API schema via Marshmallow
class VinylSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'label', 'format', 'country', 'released', 'genre', 'style', 'price']

#Singular data point return
vinyl_schema = VinylSchema()

#List of multiple objects returned
vinyl_schemas = VinylSchema(many = True)

