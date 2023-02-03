from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200),nullable = False)
    urls = db.relationship("Url",backref="user",cascade="all,delete")
    is_admin  = db.Column(db.Boolean,default = False)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(1000),nullable = False)
    platform = db.Column(db.String(20), nullable = False)
    view_count = db.Column(db.Integer,nullable = False)

