from flask.ext.wtf import Form 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from flask.ext.babel import gettext

class LoginForm(Form):
	email = StringField(gettext('Email:'), validators=[Required(), Length(1,64), Email()])
	password = PasswordField(gettext('Password:'), validators=[Required()])
	submit = SubmitField(gettext('Login:'))


class RegistrationForm(Form):
	email = StringField(gettext('Email:'),validators=[Required(), Length(1,64), Email()])

	username = StringField(gettext('Username:'), validators=[Required(), Length(1,64),
							Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
							 'Username must have only letters,'
								'numbers, dots or underscores')])
	password = PasswordField(gettext('Password:'), validators=[Required(),
								EqualTo('password2', message='Password must match.')])
	password2 = PasswordField(gettext('Password2:'), validators=[Required()])
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise validationError('Email aleady register.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise validationError('Username aleady in use.')