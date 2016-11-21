# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask.ext.login import login_required, current_user
from . import account_manager as am
from .forms import ClientInfoForm


@am.route('/workplan')
def workplan():
    return render_template('account_manager/workplan.html')


@am.route('/wpcomplete')
def wpcomplete():
    return render_template('account_manager/wpcomplete.html')


@am.route('/costofsales')
def costofsales():
    return render_template('account_manager/costofsales.html')


@am.route('/clientinfo_new')
def clientinfo_new():
    form = ClientInfoForm()
    return render_template('account_manager/clientinfo_new.html', form=form)


@am.route('/clientinfo_search')
def clientinfo_search():
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