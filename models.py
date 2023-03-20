from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from db_schema import db


class GenericModelMixin:
    def update_from_json(self, cleaned_data):
        for field, value in cleaned_data.items():
            setattr(self, field, value)
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()

    def create_from_json(self):
        errors = []
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            errors.append({'status_code': 400, 'message': 'Integrity error: item may already exist'})
        return errors


class User(db.Model, GenericModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    date_joined = db.Column(db.DateTime, server_default=func.now())
    # advertisements

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username
        }


class Advertisement(db.Model, GenericModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, server_default=func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    owner = db.relationship(User, backref=db.backref('advertisements'))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title
        }
