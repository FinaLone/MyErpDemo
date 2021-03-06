# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import render_template, redirect, url_for, jsonify, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from . import boss
from .. import db
from .forms import StatisticsWorkplanForm, ReviewAMWorkPlanForm, NotificationForm
from ..models import WorkPlan, User, Notification, ReadNotification
from ..decorators import CJsonEncoder, boss_required
import json

#统计信息，单人时间段内三项数值，全体时间段内单项数值
#时间段为了显示方便，不要弄太长，主要是保证列数不要太多就好

@boss.route('/statistics_workplan', methods=["GET", "POST"])
@boss_required
def statistics_workplan():
    form = StatisticsWorkplanForm()
    return render_template('boss/statistics_workplan.html', form=form)

#全体，一段时间，三项数值和
@boss.route('/_statistics_allam_workplan_sum')
@boss_required
def statistics_allam_workplan_sum():
    # am_id = request.args.get('am_id',0,type=int)
    startdate = request.args.get('start_date')
    enddate = request.args.get('end_date')

    searchdata=db.session.query(WorkPlan.am_id,
                     db.func.sum(WorkPlan.client_contact),
                     db.func.sum(WorkPlan.capital_increment),
                     db.func.sum(WorkPlan.volume)
                     ).filter(db.and_(WorkPlan.tommorrowdate.between(startdate,enddate),
                                   WorkPlan.flag==0)).group_by(WorkPlan.am_id).order_by(WorkPlan.am_id).all()
    am_id_name=db.session.query(User.name).filter(User.role_id==1).order_by(User.id).all()

    labels = []
    for am_name in am_id_name:
        labels.append(am_name[0])

    client_contact = []
    capital_increment = []
    volume =[]
    for data in searchdata:
        client_contact.append(data[1])
        capital_increment.append(data[2])
        volume.append(data[3])

    dict_client_contact={'fillColor' : "rgba(220,220,220,0.5)",
                        'strokeColor' : "rgba(220,220,220,0.5)",
                        'pointColor' : "rgba(220,220,220,0.5)",
                        'pointStrokeColor' : "#fff",
                        'data' : client_contact}
    dict_capital_increment={'fillColor' : "rgba(151,187,205,0.5)",
			'strokeColor' : "rgba(151,187,205,0.5)",
			'pointColor' : "rgba(151,187,205,0.5)",
			'pointStrokeColor' : "#fff",
			'data' : capital_increment}
    dict_volume={'fillColor' : "rgba(101,117,205,0.5)",
			'strokeColor' : "rgba(101,117,205,0.5)",
			'pointColor' : "rgba(101,117,205,0.5)",
			'pointStrokeColor' : "#fff",
			'data' : volume}
    client_contact = [dict_client_contact]
    capital_increment = [dict_capital_increment]
    volume = [dict_volume]

    return jsonify(labels=labels, client_contact=client_contact, capital_increment=capital_increment, volume=volume)

#单人，指定日期，三项数值
@boss.route('/review_am_workplan', methods=["GET", "POST"])
@boss_required
def review_am_workplan():
    form = ReviewAMWorkPlanForm()
    return render_template('boss/review_am_workplan.html', form=form)

@boss.route('/_review_single_am_workplan')
@boss_required
def review_single_am_workplan():
    amid = request.args.get('am_id',0,type=int)
    startdate = request.args.get('start_date')
    enddate = request.args.get('end_date')
    if startdate > enddate:
        return jsonify()

    searchdata=db.session.query(WorkPlan.client_contact,
                                WorkPlan.capital_increment,
                                WorkPlan.volume,
                                WorkPlan.todaydate).filter(db.and_(WorkPlan.tommorrowdate.between(startdate,enddate),
                                                                   WorkPlan.flag==0,
                                                                   WorkPlan.am_id==amid)
                                                           ).order_by(WorkPlan.todaydate).all()

    labels = []
    client_contact = []
    capital_increment = []
    volume =[]
    for data in searchdata:
        labels.append(json.dumps(data[3],cls=CJsonEncoder))
        client_contact.append(data[0])
        capital_increment.append(data[1])
        volume.append(data[2])

    dict_client_contact={'fillColor' : "rgba(220,220,220,0.5)",
                        'strokeColor' : "rgba(220,220,220,0.5)",
                        'pointColor' : "rgba(220,220,220,0.5)",
                        'pointStrokeColor' : "#fff",
                        'data' : client_contact}
    dict_capital_increment={'fillColor' : "rgba(151,187,205,0.5)",
			'strokeColor' : "rgba(151,187,205,0.5)",
			'pointColor' : "rgba(151,187,205,0.5)",
			'pointStrokeColor' : "#fff",
			'data' : capital_increment}
    dict_volume={'fillColor' : "rgba(101,117,205,0.5)",
			'strokeColor' : "rgba(101,117,205,0.5)",
			'pointColor' : "rgba(101,117,205,0.5)",
			'pointStrokeColor' : "#fff",
			'data' : volume}
    client_contact = [dict_client_contact]
    capital_increment = [dict_capital_increment]
    volume = [dict_volume]

    return jsonify(labels=labels, client_contact=client_contact, capital_increment=capital_increment, volume=volume)

@boss.route('/notification', methods=["GET", "POST"])
@boss_required
def notification():
    form = NotificationForm()
    publish_datetime = datetime.now()
    target_role_id = form.target.data
    if form.validate_on_submit():
        newNotification=Notification(
            publish_id = current_user.id,
            target_role_id = target_role_id,
            title = form.title.data,
            body = form.title.data,
            publish_datetime = publish_datetime
        )
        db.session.add(newNotification)
        db.session.commit()

        notification_id=db.session.query(Notification.id).filter(
            Notification.publish_datetime==publish_datetime).first()[0]
        users=db.session.query(User.id).filter(User.flag==1).all()     #默认发给所有人
        if target_role_id!=99:
            users=db.session.query(User.id).filter(
                db.and_(User.role_id==target_role_id,
                        User.flag==1)).all()
        for reader in users:
            newReadNotification=ReadNotification(
                reader_id = reader.id,
                notification_id = notification_id
            )
            db.session.add(newReadNotification)
        db.session.commit()
        flash('通知已发布')
        return redirect(url_for('boss.notification'))
    return render_template('boss/notification.html', form=form)
