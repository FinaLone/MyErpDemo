# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')


from flask.ext.wtf import Form
#from flask.ext.admin.form import widgets
from wtforms import StringField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import ClientInfo


class ClientInfoForm(Form):
    flag = SelectField('客户类型', choices=[('1','已开户'),('0','未开户')])
    name = StringField('姓名', validators=[Required(), Length(1, 64)])
    sex = StringField('性别', choices=[('0',"未知"),('1',"女"),('2',"男")])
    preference = StringField('投资偏好')
    race = StringField('民族')
    id_number = StringField('身份证号', default='')
    birthday = DateField('生日', format='%Y/%m/%d')
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

    def validate_id_number(self, field):                #验证身份证号码
        if not ClientInfo.query.filter_by(id_number=field.data).first() is None:
            raise ValidationError('身份证号已注册，请检查！')

    def validate_account_number(self, field):           #验证用户账户
        if not ClientInfo.query.filter_by(account_number=field.data).first() is None:
            raise ValidationError('用户账户已注册过，请检查！')

class ClientSearchForm(Form):
    flag = SelectField('客户类型',choices=[('1','已开户'),('0','未开户')])
    name = StringField('姓名', validators=[Required(), Length(1, 64)])
    sex = StringField('性别', default='')
    preference = StringField('投资偏好', default='')
    race = StringField('民族', default='')
    phone = StringField('电话', default='')
    submit = SubmitField('查询', default='')