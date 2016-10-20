# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, db
from ..email import send_email
from .forms import LoginForm, RegistrationForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated() \
            and not current_user.register_time \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.register_time:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            print "user_name: "+user.user_name
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('错误的用户名或者密码!')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_name=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(user.email, '确认开通账户',
                   'auth/email/confirm', user=user, token=token)

        flash('现在可以登录了！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.register_time:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('账户已确认. 谢谢！')
    else:
        flash('注册链接有误或已过期！')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))