from datetime import datetime

from flask_security import AsaList, RoleMixin, SQLAlchemyUserDatastore, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import backref, relationship


db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    authentication_token = db.Column(db.String(255))
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))

    def get_auth_token(self):
        from flask import current_app
        from itsdangerous import URLSafeTimedSerializer

        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps({'id': self.id})
        self.authentication_token = token
        db.session.commit()
        return token


class eSection(db.Model):
    __tablename__ = 'eSection'
    section_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    section_name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'))
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    updated_at = db.Column(db.DateTime, default=None)
    ebooks = db.relationship('eBooks', back_populates='esection', lazy=True)
    status = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f"{self.section_name}"


class eBooks(db.Model):
    __tablename__ = 'eBooks'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(255), nullable=False)
    book_author = db.Column(db.String(255), nullable=False)
    book_content = db.Column(db.LargeBinary, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    dateissued = db.Column(db.DateTime, nullable=True, default=None)
    returndate = db.Column(db.DateTime, nullable=True, default=None)
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'))
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    updated_at = db.Column(db.DateTime, default=None)
    sectionid = db.Column(db.Integer, db.ForeignKey('eSection.section_id'))
    esection = db.relationship('eSection', back_populates='ebooks', lazy=True)
    requested = db.relationship('Requested', back_populates='ebooks', lazy=True)
    issued = db.relationship('Issued', back_populates='ebooks', lazy=True, foreign_keys='Issued.bookid')
    status = db.Column(db.Boolean, default=True)
    DownloadPrice = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"{self.book_name}"


class Requested(db.Model):
    __tablename__ = 'requested'
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))
    bookid = db.Column(db.Integer, db.ForeignKey('eBooks.book_id'))
    requested_at = db.Column(db.DateTime, default=None)
    user = db.relationship('User', backref=db.backref('requested_books', lazy=True))
    ebooks = db.relationship('eBooks', back_populates='requested', lazy=True, foreign_keys=[bookid])
    status = db.Column(db.String(255), default='Pending')

    def __repr__(self) -> str:
        return f"{self.request_id}"


class Issued(db.Model):
    __tablename__ = 'issued'
    issue_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookid = db.Column(db.Integer, db.ForeignKey('eBooks.book_id'))
    user = db.relationship('User', backref=db.backref('issued_books', lazy=True))
    ebooks = db.relationship('eBooks', back_populates='issued', lazy=True, foreign_keys=[bookid])
    issued_at = db.Column(db.DateTime)
    return_before = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='Issued')

    def __repr__(self) -> str:
        return f"{self.issue_id}"


class Feedback(db.Model):
    __tablename__ = 'feedback'
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    feedback_message = db.Column(db.String(2000), nullable=False)
    rating_id = db.Column(Integer, primary_key=True, autoincrement=True)
    feedback_user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('eBooks.book_id'), nullable=False)
    rating_value = db.Column(Float, nullable=False)
    feedback_time = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self) -> str:
        return (
            f"Rating({self.rating_id}, Rater: {self.feedback_user_id}, "
            f"Book: {self.book_id}, Rating: {self.rating_value})"
        )


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
