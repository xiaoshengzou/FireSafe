from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask.ext.login import logout_user, login_required, current_user
from . import main
from ..models import User, Permission, SensorLog, Sensor 
from . forms import EditProfiledForm
from .. import db
from flask import request, jsonify
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    sensor_logs = SensorLog.query.order_by(SensorLog.time.desc()).limit(7).all()
    count = SensorLog.query.count()
    return render_template('index.html',sensor_logs=sensor_logs,count=count)

@main.route('/updataOption',methods=['POST'])
def updataOption():
    sensor= []
    sensors = Sensor.query.order_by(Sensor.sonmodel_id)
    for s in sensors:
        a = {
             'slaveid': s.sonmodel_id, 
             'position': s.position,
             'state': s.sensor_state
        }
        sensor.append(a)
    json = {'sensor': sensor}
    return jsonify(**json)

@main.route('/refreshLog', methods=['POST'])
@login_required
@admin_required
def refreshLog():
    slogs = []
    sensor_logs = SensorLog.query.order_by(SensorLog.time.desc()).limit(7).all()
    count = SensorLog.query.count()
    for slog in sensor_logs:
        log = {
            'name':slog.sensor_name,
            'state':slog.sensor_state,
            'time':slog.time.strftime("%Y-%m-%d %H:%M:%S")
        }
        slogs.append(log)
    json = {'slogs':slogs}

    return jsonify(**json)


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
            db.session.add(u)
            return 'ok'
        elif option == 1:
            u.understudy = True
            db.session.add(u)
            return 'ok'
        else:
            return 'fail'
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

@main.route('/moveTopOrCancel',methods=['POST'])
@login_required
@admin_required
def moveTopOrCancel():
    id = request.values.get('id', -1, type=int)
    sensor = Sensor.query.filter_by(id=id).first()
    opCode = request.values.get('opCode', 0, type=int)
    if sensor is not None:
        if opCode == 1:
            sensor.is_top = True
            db.session.add(sensor)
            return 'ok'
        elif opCode == 2:
            sensor.is_top = False
            db.session.add(sensor)
            return 'ok'
        else:
            return 'fail'
    else:
        return 'fail'

@main.route('/help')
@login_required
def help():
    return render_template('help.html')
		

