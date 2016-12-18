# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask.ext.login import login_required, current_user
from . import financial_manager as fm


@fm.route('/travel_and_entertainment_expense')
def travel_and_entertainment_expense():
    return render_template('financial_manager/travel_and_entertainment_expense.html')