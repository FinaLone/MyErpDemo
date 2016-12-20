# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, NumberRange, Optional
from .. import db
from ..models import User, Role
from datetime import datetime

class TEExpenseForm(Form):
    am_id = SelectField('员工姓名', coerce=int)
    invoice_date = DateField('开票日期')
    invoice_amount = IntegerField('发票金额', default=0)
    refund_amount = IntegerField('报销金额', default=0)
    info = TextAreaField('备注', default='请在这里输入一些文字描述信息...')
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(TEExpenseForm, self).__init__(*args, **kwargs)
        roleamid = Role.query.filter_by(name='AM').first().id
        self.am_id.choices=[(am.id, am.user_name) for am in User.query.filter_by(role_id=roleamid).all()]
        self.invoice_date.data=datetime.now().date()
