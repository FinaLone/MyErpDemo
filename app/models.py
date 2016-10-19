# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from . import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


#   用户角色表roles
class Role(db.Model):
    __tablename__ = 'TRoleInfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


#   用户表TUserInfo
class User(UserMixin, db.Model):
    __tablename__ = 'TUserInfo'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('TRoleInfo.id'))
    user_name = db.Column(db.String(64), unique=True, index=True)
    login_time = db.Column(db.DateTime)
    register_time = db.Column(db.DateTime)
    pwd_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('密码是不可读取的！')

    @password.setter
    def password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def __repr__(self):
        return '<User %r>' % self.user_name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#   注册码表TRegisterCode
class RegisterCode(db.Model):
    __tablename__ = 'TRegisterCode'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True)
    valid_flag = db.Column(db.Integer)
    expired_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.username
