# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import account_manager as am
from .. import db
from .forms import ClientInfoForm, ClientSearchForm, QuestionForm, AnswerForm
from ..models import ClientInfo, Question, Answer


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
            sex = int(form.sex.data),
            preference = form.preference.data,
            race = form.race.data,
            id_number = form.id_number.data,
            birthday = form.birthday.data,
            account_number = form.account_number.data,
            phone_1 = form.phone_1.data,
            phone_2 = form.phone_2.data,
            phone_3 = form.phone_3.data,
            qq = int(form.qq.data),
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
        flag = int(form.flag.data)
        name = form.name.data
        sex = int(form.sex.data)
        preference = form.preference.data
        race = form.race.data
        phone = form.phone.data
        #User.query.filter(User.user_name.like('%'+b+'%')).first()
        findlist = ClientInfo.query.filter(db.and_(ClientInfo.am_id==am_id,
                                                ClientInfo.flag==flag,
                                                ClientInfo.name.like("%"+name+"%"),
                                                ClientInfo.sex==sex,
                                                ClientInfo.preference.like("%"+preference+"%"),
                                                ClientInfo.race.like("%"+race+"%")
                                                )).all()        #电话先不考虑ClientInfo.phone.like("%"+phone+"%")
        if findlist==[]:
            flash("hehe")
            #return redirect(url_for('clientinfo_search'))
        flash(len(findlist))
    return render_template('account_manager/clientinfo_search.html',form=form)


@am.route('/clientinfo_net')
def clientinfo_net():
    return render_template('account_manager/clientinfo_net.html')


@am.route('/qa_list', methods=["GET", "POST"])
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