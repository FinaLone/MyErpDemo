# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import render_template, redirect, url_for, abort, flash, request, current_app
from datetime import datetime, timedelta
from . import boss
from .. import db
from ..models import WorkPlan, User

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
@boss.route('/_statistics_allam_workplan_sum')
def statistics_allam_workplan_sum(self, startdate=datetime.now().date-timedelta(days=365), enddate=datetime.now().date()):
    searchdata=db.session.query(WorkPlan.am_id,
                     db.func.sum(WorkPlan.client_contact),
                     db.func.sum(WorkPlan.capital_increment),
                     db.func.sum(WorkPlan.volume)
                     ).filter(db.and_(WorkPlan.tommorrowdate.between(startdate,enddate),
                                   WorkPlan.flag==0)).group_by(WorkPlan.am_id).all()
    am_id_name=db.session.query(User.id,User.name).filter(User.role_id==1).all()
    lables = []
    for am_name in am_id_name:
        lables.append(am_name)
    client_contact = []
    capital_increment = []
    volume =[]
    for data in searchdata:
        client_contact.append(data[1])
        capital_increment.append(data[2])
        volume.append(data[3])

    dict_client_contact='{fillColor : "rgba(220,220,220,0.5)",'\
                        +'strokeColor : "rgba(220,220,220,1)",'\
                        +'pointColor : "rgba(220,220,220,1)",'\
                        +'pointStrokeColor : "#fff",'\
                        +'data : '+client_contact+'}'
    dict_capital_increment='fillColor : "rgba(151,187,205,0.5)",'\
			+'strokeColor : "rgba(151,187,205,1)",'\
			+'pointColor : "rgba(151,187,205,1)",'\
			+'pointStrokeColor : "#fff",'\
			+'data : '+capital_increment+'}'
    dict_volume='fillColor : "rgba(101,117,205,0.5)",'\
			+'strokeColor : "rgba(101,117,205,1)",'\
			+'pointColor : "rgba(101,117,205,1)",'\
			+'pointStrokeColor : "#fff",'\
			+'data : '+volume+'}'
    datasets = [dict_client_contact,dict_capital_increment,dict_volume]
    data={'lables':lables,
          'datasets':datasets}
    return data

#单人，指定日期，三项数值
def statistics_singleam_workplan(self, amid, thatday):
    data=db.session.query(WorkPlan.am_id,
                          WorkPlan.client_contact,
                          WorkPlan.capital_increment,
                          WorkPlan.volume).filter(db.and_(WorkPlan.todaydate==thatday,
                                                  WorkPlan.flag==0)).first()
    return data
