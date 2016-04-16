from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask.ext.login import logout_user, login_required, current_user
from . import main
from ..models import User, Permission, SensorLog 
from . forms import EditProfiledForm
from .. import db
from flask import request, jsonify
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfiledForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.company = form.company.data
        db.session.add(current_user)
        #flash('Your profile has been updated.')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data = current_user.name
    form.company.data = current_user.company
    return render_template('edit_profile.html', form=form)

@main.route('/manager')
@login_required
@admin_required
def manage_user():
    understudys = User.query.filter_by(understudy=True).all()
    allusers = User.query.filter_by(understudy=False).all()
    return render_template('manage_user.html', users=understudys, allusers=allusers)

@main.route('/agreeOrFreeze', methods=['POST'])
@login_required
@admin_required
def agreeOrFreeze():
    id = request.values.get('id', 0, type=int)
    option = request.values.get('option', -1, type=int)
    u = User.query.filter_by(id=id).first()
    if u is not None:
        if option == 0:
            u.understudy = False
        elif option == 1:
            u.understudy = True
        else:
            return 'fail'
        return 'ok'
    else:
        return 'fail'


@main.route('/disagreeOrdelete', methods=['POST'])
@login_required
@admin_required
def disagreeOrdelete():
    id = request.values.get('id', 0, type=int)
    u = User.query.filter_by(id=id).first()
    if u is not None:
        db.session.delete(u)
        return 'ok'
    else:
        return 'fail'

@main.route('/help')
@login_required
def help():
    return render_template('help.html')
		