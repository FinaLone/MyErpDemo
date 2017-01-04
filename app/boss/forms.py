# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField, DateField, SelectField, TextAreaField, validators
from ..models import User, Role
from datetime import datetime, timedelta

class StatisticsWorkplanForm(Form):
    #am_id = SelectField('员工姓名', coerce=int)
    start_date = DateField('开始日期')
    end_date = DateField('结束日期')

    def __init__(self, *args, **kwargs):
        super(StatisticsWorkplanForm, self).__init__(*args, **kwargs)
        self.start_date.data=datetime.now().date()-timedelta(days=365)
        self.end_date.data=datetime.now().date()
    #添加验证函数，结束日期不能早于开始日期

class ReviewAMWorkPlanForm(Form):
    am_id = SelectField('员工姓名', coerce=int)
    start_date = DateField('开始日期')
    end_date = DateField('结束日期')

    def __init__(self, *args, **kwargs):
        super(ReviewAMWorkPlanForm, self).__init__(*args, **kwargs)
        roleamid = Role.query.filter_by(name='AM').first().id
        self.am_id.choices=[(am.id, am.name) for am in User.query.filter_by(role_id=roleamid).all()]
        self.start_date.data=datetime.now().date()-timedelta(days=365)
        self.end_date.data=datetime.now().date()
    #添加验证函数，结束日期不能早于开始日期