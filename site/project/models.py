from flask_login import UserMixin

from project import db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    path_vm = db.Column(db.String(100), default="None")
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
           return f"{self.name}; Статус: {self.status}"

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)