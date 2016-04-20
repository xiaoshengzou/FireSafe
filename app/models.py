#-*- coidng: utf-8 -*-

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db
from . import login_manager
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
# from flask import current_app

class Permission:
	USER  = 0X01
	ADMIN = 0X80
	
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref = 'role', lazy='dynamic')
	permissions = db.Column(db.Integer)
	default = db.Column(db.Boolean, default=False, index=True)

	@staticmethod
	def insert_roles():
		roles ={
		'User':(Permission.USER, True),
		'Admin':(Permission.ADMIN, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

	def __repr__(self):
		return '<Role %r>' % self.name




class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id            = db.Column(db.Integer,primary_key=True)
	email         = db.Column(db.String(64), unique=True, index=True)
	username      = db.Column(db.String(64),unique=True,index=True)
	role_id       = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	name          = db.Column(db.String(64))
	company       = db.Column(db.String(64))
	member_since  = db.Column(db.DateTime(), default=datetime.now)
	last_seen     = db.Column(db.DateTime(), default=datetime.now)
	understudy    = db.Column(db.Boolean(),default=True)

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == 'kobe@www.com':
				self.role = Role.query.filter_by(permissions=0X80).first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()

	def ping(self):
		self.last_seen = datetime.now()
		db.session.add(self)
		
	def can(self, permissions):
		return self.role is not None and \
		(self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMIN)

	def is_understudy(self):
		if self.email == 'kobe@www.com':
			self.understudy = False
		return self.understudy

    
	class AnoymusUser(AnonymousUserMixin):

		def can(self, permissions):
			return False

		def is_administrator(self):
			return False
	login_manager.anonymous_user = AnoymusUser



	@property
	def password(self): 
		raise AttributeError('password is not a readabel attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


	def __repr__(self):
		return '<Users %r>' % self.username



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))



class MainStation(db.Model):
    __tablename__ = 'mainmodels'
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(128), unique=True)
    portname  = db.Column(db.String(32),unique=True)
    is_open   = db.Column(db.Boolean(), default=False)
    sunmodels = db.relationship('SonModel', backref='station', lazy='dynamic')

    @staticmethod
    def insert_com():
    	#windows and linux
    	coms = { 'Station1': ('COM1', '/dev/ttyUSB0'),
    			 'Station2': ('COM2', '/dev/ttyUSB1'),
    			 'Station3': ('COM3', '/dev/ttyUSB2'),
    			 'Station4': ('COM4', '/dev/ttyUSB3'),
    	         'Station5': ('COM5', '/dev/ttyUSB4'),
    	         'Station6': ('COM6', '/dev/ttyUSB5')
    	       }
    	for com in coms:
    		model = MainStation.query.filter_by(name=com).first()
    		if model is None:
    			model = MainStation(name=com)
    		model.portname = coms[com][0]
    		db.session.add(model)
    	db.session.commit()


class SonModel(db.Model):
    __tablename__ = 'sonmodels'
    id            = db.Column(db.Integer, primary_key=True)
    name 		  = db.Column(db.String(128), unique=True)
    slaveaddress  = db.Column(db.Integer, unique=True)
    location      = db.Column(db.String(128))
    sensorsNumber = db.Column(db.Integer)
    main_id       = db.Column(db.Integer, db.ForeignKey('mainmodels.id'))
    is_run        = db.Column(db.Boolean(), default=False)
    sensors       = db.relationship('Sensor', backref='sonmodel', lazy='dynamic')

    def __init__(self, **kwargs):
    	super(SonModel, self).__init__(**kwargs)
    	#set default COM
    	if self.station is None:
    		self.station = MainStation.query.filter_by(portname='COM3').first()

    def getComNumber(self):
    	return self.station.portname

    def setComNumber(self, id):
    	mainstation = MainStation.query.filter_by(id=id).first()
    	if mainstation is not None:
    		self.station = mainstation
    		return True
    	else:
    		return False


class Sensor(db.Model):
	__tablename__ = 'sensors'
	id          = db.Column(db.Integer, primary_key=True)
	name		= db.Column(db.String(128), unique=True)
	location    = db.Column(db.String(128))
	slave_id    = db.Column(db.Integer)
	position    = db.Column(db.Integer)
	is_run      = db.Column(db.Boolean(), default=False)
	sonmodel_id = db.Column(db.Integer, db.ForeignKey('sonmodels.id'))


class SensorLog(db.Model):
	__tablename__ = 'sensorslog'
	id            = db.Column(db.Integer, primary_key=True)
	position      = db.Column(db.Integer)
	slave_id      = db.Column(db.Integer)
	sensor_state  = db.Column(db.String(32), default=u'unopened')
	create_time   = db.Column(db.DateTime(), default=datetime.now)
	updata_time   = db.Column(db.DateTime(), default=datetime.now)





