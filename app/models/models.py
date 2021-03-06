# -*- coding: utf-8 -*-
# @File: models.py
# @Author: byron
# @Date: 11/19/20

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    """ Base model """
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def session_commit():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return str(e)


class UserInfo(BaseModel, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(64), nullable=False)
    mobile = db.Column(db.String(16), nullable=False)
    avatar_url = db.Column(db.String(256))
    signature = db.Column(db.String(256))
    sex = db.Column(db.Enum("0", "1", "2"), default="0")  # 0: unknown, 1: Male, 2: Female
    birth_date = db.Column(db.Date)
    role_id = db.Column(db.Integer)

    def __init__(self, mobile, nickname):
        self.mobile = mobile
        self.nickname = nickname

    def add(self, user):
        db.session.add(user)
        self.session_commit()

    def update(self):
        self.session_commit()

    def to_dict(self):
        return {'id': self.id,
                'nickname': self.nickname,
                'mobile': self.mobile,
                'avatar_url': self.avatar_url,
                'signature': self.signature,
                'sex': self.sex,
                'birth_date': self.birth_date}

    def __repr__(self):
        return '<UserInfo: %r>' % self.nickname


class LoginUser(BaseModel, db.Model):
    __tablename__ = "users_login"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(16), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer)
    last_login = db.Column(db.DateTime, default=datetime.now)

    @property
    def password(self):
        return "Unreadable param"

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add(self, user):
        db.session.add(user)
        self.session_commit()

    def update(self):
        self.session_commit()

    def to_dict(self):
        return {'mobile': self.mobile,
                'user_id': self.user_id,
                'last_login': self.last_login}

    def __repr__(self):
        return '<UserInfo: %r>' % self.mobile
