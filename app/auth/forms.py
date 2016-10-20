# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, RegisterCode


class LoginForm(Form):
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[Required(), Length(1,64)])
    remember_me = BooleanField('保存登录状态')
    submit = SubmitField('登陆')


class RegistrationForm(Form):
    registercode = StringField('注册码', validators=[Required(), Length(1, 64)])   #这段Length将来决定
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z0-9_.]*$', 0,
                                          '用户名只能包含字母、'
                                          '数字、点号或者下划线')])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='两次密码输入不同.')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_registercode(self, field):
        if not RegisterCode.query.filter_by(code=field.data, valid_flag=1).first():     #没有处理失效时间
            raise ValidationError('注册码有问题!')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('用户名已被占用!')
