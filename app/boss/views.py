# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import render_template, redirect, url_for, abort, flash, request, current_app
from . import boss
from .. import db
from ..models import WorkPlan

'''
db.session.query(ClientInfo.am_id,db.func.count()).filter(ClientInfo.flag==0).group_by(ClientInfo.am_id).all()
db.session.query(ClientInfo.am_id,db.func.sum(ClientInfo.flag)).group_by(ClientInfo.am_id).all()
db.session.query(WorkPlan.am_id,db.func.sum(WorkPlan.client_contact),db.func.sum(WorkPlan.capital_increment),db.func.sum(WorkPlan.volume)).group_by(WorkPlan.am_id).all()

db.session.query(WorkPlan.am_id,db.func.sum(WorkPlan.client_contact),db.func.sum(WorkPlan.capital_increment),db.func.sum(WorkPlan.volume)).group_by(WorkPlan.am_id).all()
return--> [(1, 11, 11, 11), (2, 4, 4, 4), (3, 12, 2, 2), (4, 10, 10, 10)]

db.session.query(WorkPlan.todaydate).filter(WorkPlan.todaydate.between(thatday,today)).all()
return-->[(datetime.date(2016, 12, 13),), (datetime.date(2016, 12, 24),), (datetime.date(2016, 12, 24),)]
'''

#统计信息，单人时间段内三项数值，全体时间段内单项数值
#时间段为了显示方便，不要弄太长，主要是保证列数不要太多就好

@boss.route('/statistics_workplan', methods=["GET", "POST"])
def statistics_workplan():

    return render_template('boss/statistics_workplan.html')

#全体，一段时间，三项数值和
def statistics_allam_workplan_sum(self, startdate, enddate):
    data=db.session.query(WorkPlan.am_id,
                     db.func.sum(WorkPlan.client_contact),
                     db.func.sum(WorkPlan.capital_increment),
                     db.func.sum(WorkPlan.volume)
                     ).filter(db.and_(WorkPlan.tommorrowdate.between(startdate,enddate),
                                   WorkPlan.flag==0)).group_by(WorkPlan.am_id).all()
    return data

#单人，指定日期，三项数值
def statistics_singleam_workplan(self, amid, thatday):
    data=db.session.query(WorkPlan.am_id,
                          WorkPlan.client_contact,
                          WorkPlan.capital_increment,
                          WorkPlan.volume).filter(db.and_(WorkPlan.todaydate==thatday,
                                                  WorkPlan.flag==0)).first()
    return data
