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

class ChangePasswordForm(Form):
    old_password = PasswordField('原密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='两次密码输入必须相同！')])
    password2 = PasswordField('确认新密码', validators=[Required()])
    submit = SubmitField('确认修改密码')


class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重设密码')


class PasswordResetForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('设置为新密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱填写错误或未注册！')


class ChangeEmailForm(Form):
    email = StringField('新的邮箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('你的密码', validators=[Required()])
    submit = SubmitField('重设邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('这个邮件地址已经被注册过了！')
