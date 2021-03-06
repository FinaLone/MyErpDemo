# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
import json
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, abort, flash, request, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import account_manager as am
from .. import db
from .forms import ClientInfoForm, ClientSearchForm, QuestionForm, AnswerForm, WorkPlanForm, WorkCompleteForm
from ..models import ClientInfo, Question, Answer, WorkPlan
from ..decorators import am_required


@am.route('/workplan', methods=["GET", "POST"])
@am_required
def workplan():
    form = WorkPlanForm()
    if form.validate_on_submit():
        my_amid = current_user.id
        newworkplan = WorkPlan(
            flag = 0,
            am_id = my_amid,
            todaydate = datetime.now().date(),
            tommorrowdate = datetime.now().date() + timedelta(days=1),
            client_contact = form.client_contact.data,
            capital_increment = form.capital_increment.data,
            volume = form.volume.data,
            other_info = form.other_info.data
        )
        db.session.add(newworkplan)
        db.session.commit()
        flash('工作计划添加成功！')
        return redirect(url_for('account_manager.workplan'))
    return render_template('account_manager/workplan.html', form=form)


@am.route('/wpcomplete', methods=["GET", "POST"])
@am_required
def wpcomplete():
    my_amid = current_user.id
    todaydate = datetime.now().date()
    yesterdayplan = WorkPlan.query.filter(db.and_(WorkPlan.am_id==my_amid,
                                                  WorkPlan.tommorrowdate==todaydate,
                                                  WorkPlan.flag==0)).first()

    if yesterdayplan.todaydate==None:
        flash("没有今天的工作计划！")
        # form.plan_client_contact.data = todaydate - timedelta(days=1)
        # form.plan_capital_increment.data = 0
        # form.plan_volume.data = 0
        # form.plan_other_info.data = ""
        # return render_template('account_manager/wpcomplete.html', form=form)      #修改这里
        return redirect(url_for('account_manager.wpcomplete'))

    form = WorkCompleteForm()
    form.plan_client_contact.data = yesterdayplan.client_contact
    form.plan_capital_increment.data = yesterdayplan.capital_increment
    form.plan_volume.data = yesterdayplan.volume
    form.plan_other_info.data = yesterdayplan.other_info

    if form.validate_on_submit():
        complete_workplan = WorkPlan(
            flag = 1,
            am_id = my_amid,
            todaydate = datetime.now().date(),
            tommorrowdate = datetime.now().date() + timedelta(days=1),
            client_contact = form.complete_client_contact.data,
            capital_increment = form.complete_capital_increment.data,
            volume = form.complete_volume.data,
            other_info = form.complete_other_info.data
        )       #这里有个问题，就是只考虑了添加的情况，没有修改的情况，这样在数据库中会出现重复
        db.session.add(complete_workplan)
        db.session.commit()
        flash('工作计划完成情况已录入！')
        return redirect(url_for('account_manager.wpcomplete'))
    return render_template('account_manager/wpcomplete.html', form=form)



@am.route('/costofsales')
def costofsales():
    return render_template('account_manager/wpcomplete.html')


@am.route('/clientinfo_new', methods=['GET', 'POST'])
@am_required
def clientinfo_new():
    form = ClientInfoForm()
    if form.validate_on_submit():
        my_amid = current_user.id
        newclientinfo = ClientInfo(
            am_id = my_amid,
            flag = int(form.flag.data),
            name = form.name.data,
            sex = int(form.sex.data),
            preference = form.preference.data,
            race = form.race.data,
            id_number = form.id_number.data,
            birthday = form.birthday.data,
            account_number = int(form.account_number.data),
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
        print current_user.name +" get "+ newclientinfo.name        #将来注释掉
        db.session.add(newclientinfo)
        db.session.commit()
        flash('客户信息添加成功！')

        return redirect(url_for('account_manager.clientinfo_new'))
    return render_template('account_manager/clientinfo_new.html', form=form)


@am.route('/clientinfo_search', methods=['GET', 'POST'])
@am_required
def clientinfo_search():
    form = ClientSearchForm()
    return render_template('account_manager/clientinfo_search.html',form=form)

@am.route('/clientinfo_search_sql', methods=['GET', 'POST'])
@am_required
def clientinfo_search_sql():
    data = request.get_data()
    data = json.loads(data)
    am_id = current_user.id
    findlist = ClientInfo.query.filter(db.and_(ClientInfo.am_id == am_id,
                                        ClientInfo.flag==int(data['flag']),
                                        ClientInfo.name.like("%"+data['name']+"%"),
                                        ClientInfo.sex==data['sex'],
                                        ClientInfo.preference.like("%"+data['preference']+"%"),
                                        ClientInfo.race.like("%"+data['race']+"%"),
                                        ClientInfo.phone_1.like("%"+data['phone']+"%"),
                                        ClientInfo.am_id==current_user.id
                                        )).all()        #电话先不考虑ClientInfo.phone.like("%"+phone+"%")
    return_data = ''
    return_data += '{len:'
    return_data += str(len(findlist))
    return_data += ',data:['
    if len(findlist) is not 0:
        for item in findlist:
            return_data += json.dumps(item.to_json())
            return_data += ','

        return_data = return_data[:-1]
    return_data += ']}'
    return return_data

@am.route('/clientinfo_change/<client_id>', methods=['GET', 'POST'])
@am_required
def clientinfo_change(client_id):
    client_info = ClientInfo.query.filter_by(id=client_id).first()
    if client_info is None:
        abort(404)
    form = ClientInfoForm()
    if form.validate_on_submit():
        client_info.flag = int(form.flag.data)
        print(form.flag.data)
        client_info.name = form.name.data
        client_info.sex = int(form.sex.data)
        client_info.preference = form.preference.data
        client_info.race = form.race.data
        client_info.id_number = form.id_number.data
        #client_info.birthday = form.birthday.data
        client_info.account_number = int(form.account_number.data)
        client_info.phone_1 = form.phone_1.data
        client_info.phone_2 = form.phone_2.data
        client_info.phone_3 = form.phone_3.data
        client_info.qq = form.qq.data
        client_info.weixin = form.weixin.data
        client_info.email = form.email.data
        client_info.occupation = form.occupation.data
        print(form.occupation.data)
        client_info.workplace = form.workplace.data
        client_info.home = form.home.data
        client_info.hobby = form.hobby.data
        db.session.commit()
        flash('保存成功！')
        #return redirect(url_for('.clientinfo_change', form=form, client_info=client_info))
    return render_template('account_manager/clientinfo_change.html', form=form, client_info=client_info)

@am.route('/clientinfo_change_sql', methods=['GET', 'POST'])
@am_required
def clientinfo_change_sql():
    data = request.get_data()
    data = json.loads(data)
    am_id = current_user.id
    findlist = ClientInfo.query.filter(ClientInfo.id == int(data['id'])).all()
    return_data = ''
    return_data += '{len:'
    return_data += str(len(findlist))
    return_data += ',data:['
    if len(findlist) is not 0:
        for item in findlist:
            return_data += json.dumps(item.to_json())
            return_data += ','

        return_data = return_data[:-1]
    return_data += ']}'
    return return_data

@am.route('/clientinfo_net')
@am_required
def clientinfo_net():
    return render_template('account_manager/clientinfo_net.html')


@am.route('/qa_list', methods=["GET", "POST"])
@am_required
def qa_list():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(question)
        return redirect(url_for('.qa_list'))
    #questions = Question.query.order_by(Question.timestamp.desc()).all()

    page = request.args.get('page',1,type=int)
    pagination = Question.query.order_by(Question.timestamp.desc()).paginate(
        page, per_page=10, error_out=False)
    questions = pagination.items
    return render_template('account_manager/qa_list.html',  form=form, questions=questions, pagination=pagination)


@am.route('/qa_new', methods=["GET", "POST"])
@am_required
def qa_new():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(question)
        return redirect(url_for('.qa_list'))
    return render_template('account_manager/qa_new.html', form=form)

@am.route('/qa/<qno>', methods=["GET", "POST"])
@am_required
def qa_detail(qno):
    question = Question.query.filter_by(id=qno).first()
    if question is None:
        abort(404)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(body = form.body.data,
                          question = question,
                          author = current_user._get_current_object())
        db.session.add(answer)
        flash('已回答')
        return redirect(url_for('.qa_detail', qno=question.id))
    answers = question.answers.order_by(Answer.timestamp.asc())
    return render_template('account_manager/qa_detail.html', question=question, form = form, answers = answers)

