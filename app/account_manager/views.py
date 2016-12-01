# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import account_manager as am
from .. import db
from .forms import ClientInfoForm, ClientSearchForm
from ..models import ClientInfo


@am.route('/workplan')
def workplan():
    return render_template('account_manager/workplan.html')


@am.route('/wpcomplete')
def wpcomplete():
    return render_template('account_manager/wpcomplete.html')


@am.route('/costofsales')
def costofsales():
    return render_template('account_manager/costofsales.html')


@am.route('/clientinfo_new', methods=['GET', 'POST'])
def clientinfo_new():
    form = ClientInfoForm()
    if form.validate_on_submit():
        my_amid = current_user.id
        newclientinfo = ClientInfo(
            am_id = my_amid,
            flag = int(form.flag.data),
            name = form.name.data,
            sex = form.sex.data,
            preference = form.preference.data,
            race = form.race.data,
            id_number = form.id_number.data,
            birthday = form.birthday.data,
            account_number = form.account_number.data,
            phone_1 = form.phone_1.data,
            phone_2 = form.phone_2.data,
            phone_3 = form.phone_3.data,
            qq = form.qq.data,
            weixin = form.weixin.data,
            email = form.email.data,
            occupation = form.occupation.data,
            workplace = form.workplace.data,
            home = form.home.data,
            hobby = form.hobby.data
        )
        db.session.add(newclientinfo)
        db.session.commit()
        flash('客户信息添加成功！')
        return redirect(url_for('account_manager.clientinfo_new'))
    return render_template('account_manager/clientinfo_new.html', form=form)


@am.route('/clientinfo_search', methods=['GET', 'POST'])
def clientinfo_search():
    form = ClientSearchForm()
    if form.validate_on_submit():
        am_id = current_user.id
        flag = form.flag.data
        name = form.name.data
        sex = form.sex.data
        preference = form.preference.data
        race = form.race.data
        phone = form.phone.data
    #User.query.filter(User.user_name.like('%'+b+'%')).first()



    return render_template('account_manager/clientinfo_search.html')


@am.route('/clientinfo_net')
def clientinfo_net():
    return render_template('account_manager/clientinfo_net.html')


@am.route('/qa_list')
def qa_list():
    return render_template('account_manager/qa_list.html')


@am.route('/qa_new')
def qa_new():
    return render_template('account_manager/qa_new.html')