from app.models import db
from flask_user import UserMixin

class Member(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default=db.sql.True_())
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary='member_roles')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
