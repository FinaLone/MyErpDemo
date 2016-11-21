# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')


from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError


class ClientInfoForm(Form):
    name = StringField('姓名', validators=[Required(), Length(1, 64)])
    sex = StringField('性别')
    preference = StringField('投资偏好')
    race = StringField('民族')
    id_number = StringField('身份证号', default='')
    birthday = DateField('生日')
    account_number = StringField('交易账号', default='', validators=[Regexp('^[0-9][0-9]*$', 0, '用户账户只能是数字')])
    phone_1 = StringField('常用电话1')
    phone_2 = StringField('常用电话2')
    phone_3 = StringField('常用电话3')
    qq = StringField('QQ')
    weixin = StringField('微信')
    email = StringField('电子邮箱', validators=[Required(), Length(1, 64), Email()])
    occupation = StringField('职业')
    workplace = StringField('工作单位')
    home = StringField('家庭住址')
    hobby = StringField('业余爱好')
    submit = SubmitField('保存')

    def validate_id_number(self, field):
        pass

    def validate_account_number(self, field):
        pass