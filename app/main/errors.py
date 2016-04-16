from flask import render_template
from . import main

#note-3

@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_sever_error(e):
	return render_template('500.html'), 500

@main.app_errorhandler(403)
def internal_sever_error(e):
    return render_template('403.html'), 403

@main.app_errorhandler(401)
def internal_sever_error(e):
    return render_template('401.html'), 401

@main.route('/errors')
def tip():
    return render_template('understudy.html')