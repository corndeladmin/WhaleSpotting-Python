from app.models import db

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
