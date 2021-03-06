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
    #Travel and entertainment expense
    T_E_EXPENSE = 0x10

    ACCOUNTMANAGER = 0x0F
    FINANCIALMANAGER = 0x10
    ADMINISTER = 0x80
    BOSS = 0x70


#   用户角色表roles
class Role(db.Model):
    __tablename__ = 'TRoleInfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index= True)
    name_chinese = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')


    @staticmethod
    #insert_droles函数在添加新的职务时需要在shell里面执行一次
    def insert_roles():
        roles = {
            'SuperAdmin': (0xff, False, unicode('管理员')),
            'AM':(Permission.ACCOUNTMANAGER, False, unicode('客户经理')),
            'FM':(Permission.FINANCIALMANAGER, False, unicode('财务')),
            'BOSS':(Permission.BOSS, False, unicode('总经理'))
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            role.name_chinese = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


#   用户表TUserInfo
class User(UserMixin, db.Model):#用shell插入新用户的时候，一定要注意不要忽略confirmed一项
    __tablename__ = 'TUserInfo'
    id = db.Column(db.Integer, primary_key=True)                    #用户编号,最好是自动生成，不能修改
    flag = db.Column(db.Integer, default=1)                         #可用为1，冻结为0
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
    question = db.relationship('Question', backref='author', lazy='dynamic')
    answer = db.relationship('Answer', backref='author', lazy='dynamic')
    clients = db.relationship('ClientInfo', backref='am', lazy='dynamic')
    workplan = db.relationship('WorkPlan', backref='am', lazy='dynamic')
    teexpenxe_fm = db.relationship('TEExpense', primaryjoin='User.id==TEExpense.fm_id', backref='fm', lazy='dynamic')
    teexpenxe_am = db.relationship('TEExpense', primaryjoin='User.id==TEExpense.am_id', backref='am', lazy='dynamic')
    notification = db.relationship('Notification', backref='publisherid', lazy='dynamic')
    readnotification = db.relationship('ReadNotification', backref='readerid', lazy='dynamic')

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

    def is_accountmanager(self):
        return self.can(Permission.ACCOUNTMANAGER)

    def is_financialmanager(self):
        return self.can(Permission.FINANCIALMANAGER)

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

#客户信息表
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
    qq = db.Column(db.String)                                              #QQ
    weixin = db.Column(db.String)                                           #微信
    email = db.Column(db.String)                                            #email
    occupation = db.Column(db.String)                                       #职业
    workplace = db.Column(db.String)                                        #工作单位
    home = db.Column(db.String)                                             #家庭住址
    hobby = db.Column(db.String)                                            #业余爱好

    def __repr__(self):
        return '<CInfo: %r : %r>' % (self.am_id, self.name)

    def to_json(self):
        return {
            'id': self.id,
            'am_id': self.am_id,
            'flag': self.flag,
            'name': self.name,
            'sex': self.sex,
            'preference': self.preference,
            'race': self.race,
            'id_number': self.id_number,
            'birthday': self.birthday.strftime('%Y-%m-%d'),
            'account_number': self.account_number,
            'phone_1': self.phone_1,
            'phone_2': self.phone_2,
            'phone_3': self.phone_3,
            'qq': self.qq,
            'weixin': self.weixin,
            'email': self.email,
            'occupation': self.occupation,
            'workplace': self.workplace,
            'home': self.home,
            'hobby': self.hobby
        }

# 问题列表 luhao add 16.11.17
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('TUserInfo.id'))

    answers = db.relationship('Answer', backref='question', lazy='dynamic')


#评论  luhao add 16.11.17
class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('TUserInfo.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    #编辑器
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'strong']

#工作计划
class WorkPlan(db.Model):
    __tablename__ = 'workplan'
    id = db.Column(db.Integer, primary_key = True, index=True)
    flag = db.Column(db.Integer)                                            #表示计划或者完成情况0是计划，1是完成
    am_id = db.Column(db.Integer, db.ForeignKey('TUserInfo.id'))
    todaydate = db.Column(db.DATE)
    tommorrowdate = db.Column(db.DATE)
    client_contact = db.Column(db.Integer)
    capital_increment = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    other_info = db.Column(db.Text)

    def __repr__(self):
        return '<WorkPlan id:%r--flag:%r--date:%r>' % (self.am_id, self.flag, self.todaydate.strftime('%Y-%m-%d'))
    def yanzheng(self):
        #这里得有一个对同一个user对同一个日期只能存在一条记录的验证功能
        #还得有一个没有连续记录时候的补充功能
        pass
    def xiugaijintian(self,jintian,mingtian):
        self.todaydate=jintian
        self.tommorrowdate=mingtian
        #函数用于修改时间，实用后删除

class TEExpense(db.Model):
    __tablename__ = 'teexpense'
    id = db.Column(db.Integer, primary_key=True, index=True)
    fm_id = db.Column(db.Integer, db.ForeignKey('TUserInfo.id'))
    am_id = db.Column(db.Integer, db.ForeignKey('TUserInfo.id'))
    invoice_date = db.Column(db.DATE)                   #开票日期
    todaydate = db.Column(db.DATE)                      #报销日期
    invoice_amount = db.Column(db.Integer)              #发票金额
    refund_amount = db.Column(db.Integer)               #报销金额
    info = db.Column(db.Text)                           #备注

    def __reper__(self):
        return 'fm: %r -- am: %r' % (self.fm_id, self.am_id)

class Notification(db.Model):
    __tablename__ = 'Notification'
    id = db.Column(db.Integer, primary_key=True, index=True)
    publish_id = db.Column(db.Integer, db.ForeignKey('TUserInfo.id'))
    target_role_id = db.Column(db.Integer)
    title = db.Column(db.String)
    body = db.Column(db.Text)
    publish_datetime = db.Column(db.DateTime)

    target = db.relationship('ReadNotification', backref='Notification', lazy='dynamic')

class ReadNotification(db.Model):
    __tablename__ = 'ReadNotification'
    id = db.Column(db.Integer, primary_key=True, index=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('TUserInfo.id'))
    notification_id = db.Column(db.Integer, db.ForeignKey('Notification.id'))
    confirmed = db.Column(db.Boolean, default=False)
    read_datetime = db.Column(db.DateTime)

