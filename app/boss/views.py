# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from . import boss

'''
db.session.query(ClientInfo.am_id,db.func.count()).filter(ClientInfo.flag==0).group_by(ClientInfo.am_id).all()
db.session.query(ClientInfo.am_id,db.func.sum(ClientInfo.flag)).group_by(ClientInfo.am_id).all()
db.session.query(WorkPlan.am_id,db.func.sum(WorkPlan.client_contact),db.func.sum(WorkPlan.capital_increment),db.func.sum(WorkPlan.volume)).group_by(WorkPlan.am_id).all()
'''



@boss.route('/statistics_workplan', methods=["GET", "POST"])
def statistics_workplan():
    '''

    db.session.query(WorkPlan.am_id,db.func.sum(WorkPlan.client_contact),db.func.sum(WorkPlan.capital_increment),db.func.sum(WorkPlan.volume)).group_by(WorkPlan.am_id).all()
    return--> [(1, 11, 11, 11), (2, 4, 4, 4), (3, 12, 2, 2), (4, 10, 10, 10)]
    '''
    pass