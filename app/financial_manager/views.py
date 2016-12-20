# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask.ext.login import login_required, current_user
from . import financial_manager as fm
from .forms import TEExpenseForm
from .. import db
from ..models import TEExpense
from datetime import datetime


@fm.route('/travel_and_entertainment_expense', methods=["GET", "POST"])
def travel_and_entertainment_expense():
    form = TEExpenseForm()
    my_id = current_user.id
    print '01'
    if form.validate_on_submit():
        print '0'
        teexpense = TEExpense(
            fm_id = my_id,
            am_id = int(form.am_id.data),
            invoice_date = form.invoice_date.data,
            todaydate = datetime.now().date(),
            invoice_amount = form.invoice_amount.data,
            refund_amount = form.refund_amount.data,
            info = form.info.data
        )
        db.session.add(teexpense)
        print "1"
        db.session.commit()
        print "2"
        flash('报销内容录入成功！')
        print "3"
        return redirect(url_for('financial_manager.travel_and_entertainment_expense'))
    return render_template('financial_manager/travel_and_entertainment_expense.html', form=form)