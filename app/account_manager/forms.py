# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')


from flask.ext.wtf import Form
#from flask.ext.admin.form import widgets
from wtforms import StringField, IntegerField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, NumberRange, Optional
from wtforms import ValidationError
from ..models import ClientInfo


class ClientInfoForm(Form):
    flag = SelectField('客户类型', choices=[('1','已开户'),('0','未开户')], default='0')
    name = StringField('姓名', validators=[Required(), Length(1, 64)])
    sex = SelectField('性别', choices=[('0',"未知"),('1',"女"),('2',"男")], default='0')
    preference = StringField('投资偏好')
    race = StringField('民族')
    id_number = StringField('身份证号', default='')
    birthday = DateField('生日', format='%Y-%m-%d', validators=[Optional()])
    account_number = StringField('交易账号', default='1233211234567', validators=[Regexp('^[0-9][0-9]*$', 0, '用户账户只能是数字')])
        #account_number根据具体字符长度来验证
    phone_1 = StringField('常用电话1')
    phone_2 = StringField('常用电话2')
    phone_3 = StringField('常用电话3')
    qq = StringField('QQ')
    weixin = StringField('微信')
    email = StringField('电子邮箱')     #, validators=[Required(), Length(1, 64), Email()]
    occupation = StringField('职业')
    workplace = StringField('工作单位')
    home = StringField('家庭住址')
    hobby = StringField('业余爱好')
    submit = SubmitField('保存')

    def validate_id_number(self, field):                #验证身份证号码
        if not ClientInfo.query.filter_by(id_number=field.data).first() is None:
            if field.data!="":
                raise ValidationError('身份证号已注册，请检查！')

    def validate_account_number(self, field):           #验证用户账户
        if not ClientInfo.query.filter_by(account_number=field.data).first() is None:
            if field.data!="1233211234567":
                raise ValidationError('用户账户已注册过，请检查！')

class ClientSearchForm(Form):
    flag = SelectField('客户类型',choices=[('1','已开户'),('0','未开户')], default='0')
    name = StringField('姓名', validators=[Required(), Length(1, 64)], default='')
    sex = SelectField('性别', choices=[('0',"未知"),('1',"女"),('2',"男")], default='0')
    preference = StringField('投资偏好', default='')
    race = StringField('民族', default='')
    phone = StringField('电话', default='')
    #submit = SubmitField('查询', default='')

#发布文章/提问表单
class QuestionForm(Form):
   title =  StringField('标题', validators=[Required()])
   body = TextAreaField('详细描述' , validators=[Required()])
   submit = SubmitField('提交')

#评论表单
class AnswerForm(Form):
    body = TextAreaField('回答', validators=[Required()])
    submit = SubmitField('提交')

#工作计划录入
class WorkPlanForm(Form):
    client_contact = IntegerField('拜访，电话联系客户数量', validators=[Required(), NumberRange(min=0)])
    capital_increment = IntegerField('客户新增资金量', validators=[Required(), NumberRange(min=0)])
    volume = IntegerField('成交量', validators=[Required(), NumberRange(min=0)])
    other_info = TextAreaField('其他')
    submit = SubmitField('提交')

#计划任务完成情况
class WorkCompleteForm(Form):
    plan_client_contact = IntegerField('拜访，电话联系客户计划数')
    plan_capital_increment = IntegerField('客户新增资金计划数')
    plan_volume = IntegerField('计划成交量')
    plan_other_info = TextAreaField('其他计划')

    complete_client_contact = IntegerField('拜访，电话联系客户完成数量', validators=[Required(), NumberRange(min=0)])
    complete_capital_increment = IntegerField('客户新增资金完成量', validators=[Required(), NumberRange(min=0)])
    complete_volume = IntegerField('实际成交量', validators=[Required(), NumberRange(min=0)])
    complete_other_info = TextAreaField('其他完成事项')

    submit = SubmitField('提交')


