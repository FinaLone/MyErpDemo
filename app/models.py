# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from . import db, login_manager
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


#   用户权限表
class Permission:
    WORKPLAN = 0x01
    CLIENTINFO = 0x02

    ADMINISTER = 0x80


#   用户角色表roles
class Role(db.Model):
    __tablename__ = 'TRoleInfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index= True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'SuperAdmin': (0xff, False),
            'AM':(Permission.WORKPLAN |
                  Permission.CLIENTINFO, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


#   用户表TUserInfo
class User(UserMixin, db.Model):
    __tablename__ = 'TUserInfo'
    id = db.Column(db.Integer, primary_key=True)                    #用户编号,最好是自动生成，不能修改
                                                                    #如果有冻结账户的需要，另设flag位
    role_id = db.Column(db.Integer, db.ForeignKey('TRoleInfo.id'))
    email = db.Column(db.String(64), unique=True, index=True)
    user_name = db.Column(db.String(64), unique=True, index=True)   #登陆用用户名
    login_time = db.Column(db.DateTime, default=datetime.now())     #最后一次登录时间
    register_time = db.Column(db.DateTime, default=datetime.now())  #注册时间
    pwd_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))                                 #姓名
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))                             #籍贯
    about_me = db.Column(db.Text())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('密码是不可读取的！')

    @password.setter
    def password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.user_name

#   默认用户
class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

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
        return '<code %r>' % self.code


class ClientInfo(db.Model):
    __tablename__ = 'TClientInfo'
    id = db.Column(db.Integer, primary_key=True, index=True)
    am_id = db.Column(db.Integer, db.ForeignKey('TUserInfo.id'))
    flag = db.Column(db.Integer, default=0)                                 #标志位，默认为0
    name = db.Column(db.String)                                             #姓名,默认为未知
    sex = db.Column(db.Integer, default=0)                                  #性别，1为女2为男0为未知
    preference = db.Column(db.String)                                       #投资偏好
    race = db.Column(db.String)                                             #民族,默认为汉
    id_number = db.Column(db.String, unique=True)                           #身份证号
    birthday = db.Column(db.DATE)                                           #出生日期
    account_number = db.Column(db.Integer)                                  #交易账号
    phone_1 = db.Column(db.String)                                          #常用电话1
    phone_2 = db.Column(db.String)                                          #常用电话2
    phone_3 = db.Column(db.String)                                          #常用电话3
    qq = db.Column(db.Integer)                                              #QQ
    weixin = db.Column(db.String)                                           #微信
    email = db.Column(db.String)                                            #email
    occupation = db.Column(db.String)                                       #职业
    workplace = db.Column(db.String)                                        #工作单位
    home = db.Column(db.String)                                             #家庭住址
    hobby = db.Column(db.String)                                            #业余爱好

    def __repr__(self):
        return '<客户: %r>' % self.name

