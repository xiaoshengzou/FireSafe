# coding:utf-8 


from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment 
from flask.ext.sqlalchemy import SQLAlchemy 
from config import config
from flask.ext.login import LoginManager
from app.shared import db

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.view = 'auth.login'



def create_app(config_name):
	#note_1
	app = Flask(__name__)

	
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	
	bootstrap.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	#register blueprint
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .sensor import sensor as sensor_blueprint
	app.register_blueprint(sensor_blueprint, url_prefix='/sensor')
	

	return app