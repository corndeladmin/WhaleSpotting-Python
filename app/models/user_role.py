from app.models import db
from app.models.user import Member
from app.models.role import Role

class MemberRole(db.Model):
    __tablename__ = 'member_roles'
    id = db.Column(db.Integer(), primary_key=True)
    member_id = db.Column(db.Integer(), db.ForeignKey(Member.id, ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(Role.id, ondelete='CASCADE'))

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
