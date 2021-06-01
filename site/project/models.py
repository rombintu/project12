from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'test'

    id_user = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    user_status = db.Column(db.String(10), default="false")
    vm_status = db.Column(db.String(10), default="false")
    pub_key_status = db.Column(db.String(10), default="false")
    ip_vm = db.Column(db.String(100), default="false")


