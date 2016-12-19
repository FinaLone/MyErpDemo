# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, NumberRange, Optional
from .. import db
from ..models import User, Role

class TEExpenseForm(Form):
    am_id = SelectField('员工姓名', coerce=int)

    def __init__(self, *args, **kwargs):
        super(TEExpenseForm, self).__init__(*args, **kwargs)
        roleamid = Role.query.filter_by(name='AM').first().id
        self.am_id.choices=[(am.id, am.user_name) for am in User.query.filter_by(role_id=roleamid).all()]

