from sqlalchemy import desc

from db import db


class ClipModel(db.Model):
    __tablename__ = 'clips'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    link_yt = db.Column(db.String)
    link_img = db.Column(db.String)
    added = db.Column(db.Integer)
    score = db.Column(db.Integer)

    comments = db.relationship('CommentModel', backref='clip', lazy='dynamic')

    @classmethod
    def find_by_id(cls, clip_id):
        return cls.query.filter_by(id=clip_id).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def newest(cls, n):
        return cls.query.order_by(desc(cls.added)).limit(n).all()

    @classmethod
    def highest_rated(cls, n):
        return cls.query.order_by(desc(cls.score)).limit(n).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
