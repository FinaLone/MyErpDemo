# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import Role, User
from ..decorators import admin_required


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(user_name=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)

        filename = form.avatar.data.filename
        app = current_app._get_current_object()
        form.avatar.data.save(os.path.join(app.config['AVATAR_FOLDER'], filename))

        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.user_name))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.user_name = form.user_name.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', user_name=user.user_name))
    form.email.data = user.email
    form.user_name.data = user.user_name
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

"""


def allowed_file(filename):
    app = current_app._get_current_object()
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@main.route('/upload_avatar', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    app = current_app._get_current_object()
    if request.method == 'POST':
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~post~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Photo saved.")
            return redirect(url_for('.user', username=current_user.user_name))
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~get~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    return redirect(url_for('upload_avatar'))
    return redirect(url_for('.user', username=current_user.user_name))


"""