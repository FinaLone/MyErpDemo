# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask.ext.login import login_required, current_user
from . import account_manager as am


@am.route('/workplan')
def workplan():
    return render_template('account_manager/workplan.html')


@am.route('/wpcomplete')
def wpcomplete():
    return render_template('account_manager/wpcomplete.html')