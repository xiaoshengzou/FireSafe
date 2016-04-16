# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash 
from . import auth
from flask.ext.login import login_user
from . import auth
from ..models import User 
from .forms import LoginForm
from .forms import RegistrationForm
from flask.ext.login import logout_user, login_required, current_user
from .. import db


@auth.before_app_request
def before_request():
	if current_user.is_authenticated():
		current_user.ping()

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			if user.is_understudy():
				return redirect(url_for('auth.tip'))
			else:
			    login_user(user)
			    return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password')
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	#flash('You have been logged out.')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		return redirect(url_for('auth.login'))

	return render_template('auth/register.html', form=form)

@auth.route('/tip')
def tip():
	return render_template('auth/tip.html')


