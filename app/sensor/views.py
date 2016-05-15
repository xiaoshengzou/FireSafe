#-*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from . import sensor
from ..models import MainStation, SonModel, Sensor, SensorLog
from .forms import SonModelForm, SensorForm
from .. import db
from flask.ext.login import login_required
from ..decorators import admin_required, permission_required
from flask import jsonify

@sensor.route('/createSonModel',methods=['GET', 'POST'])
@login_required
@admin_required
def createSonModel():
    form = SonModelForm()
    if form.validate_on_submit():
        mainstation = MainStation.query.filter_by(id=form.parentModel.data).first()
        sonmodels = mainstation.sonmodels.all()
        sladdress = []
        for s in sonmodels:
            sladdress.append(s.slaveaddress)
        if SonModel.query.filter_by(name=form.sonModelName.data).first():
            flash('This name is using!')
        elif form.slaveaddress.data in sladdress:
            flash('This slaveaddress is using!')
        else:
            sonmodel = SonModel(name=form.sonModelName.data,
                                location=form.location.data,
                                sensorsNumber=form.numSensor.data,
                                slaveaddress=form.slaveaddress.data
                                )
            if not sonmodel.setComNumber(form.parentModel.data):
                flash('Setting Fail')
            db.session.add(sonmodel)
            return redirect(url_for('sensor.display'))
            
    return render_template('createSonModel.html', form=form)


@sensor.route('/display')
@login_required
def display():
    sonmodel = SonModel.query.filter_by(is_run=False).all()
    if sonmodel is not None:
        for s in sonmodel:
            s.is_run = True
            count = 0
            while count < s.sensorsNumber:
                sname = 'Sensor_'+str(s.id)+'_'+str(count+1)
                sensor = Sensor(name=sname, location='default', sonmodel=s, position=2*count)
                db.session.add(sensor)
                count += 1
            db.session.add(s)
            db.session.commit()
    sonmodels = SonModel.query.all()
    sensors = []
    for s in sonmodels:
        smodel_sensors = s.sensors.all()        #acquire of sonmodel's all sensor 
        if smodel_sensors:                      #judge have sensors
            sensors.append(smodel_sensors)
    return render_template('displaysensor.html', sensors=sensors, sonmodels=sonmodels)

@sensor.route('/createSensor/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def createSensor(id):
    form = SensorForm()
    if form.validate_on_submit():
        sensor = Sensor.query.filter_by(id=id).first()
        if sensor:
            if Sensor.query.filter_by(name=form.sensorName.data).first():
                flash('This name is using.')
            else:
                sensor.name = form.sensorName.data
                sensor.location = form.location.data
                if not sensor.is_run:
                    sensor.is_run = True
                db.session.add(sensor)
                return redirect(url_for('sensor.display'))
    return render_template('createSensor.html', form=form)

@sensor.route('/topdisplay', methods=['GET', 'POST'])
@login_required
@admin_required
def topdisplay():
    page = request.args.get('page', 1, type=int)
    pagination = Sensor.query.order_by(Sensor.create_time.desc()).paginate(page,per_page=10,error_out=False)
    sensors = pagination.items
    return render_template('topdisplay.html',sensors=sensors,pagination=pagination)

@sensor.route('/sensortable', methods=['GET', 'POST'])
@login_required
@admin_required
def displaysensortable():
    page = request.args.get('page', 1, type=int)
    pagination = SensorLog.query.order_by(SensorLog.time.desc()).paginate(page,
                                per_page=10, error_out=False)
    slogs = pagination.items
    return render_template('sensortable.html',slogs=slogs, pagination=pagination)

@sensor.route('/deleteSensor', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteSensor():
    id = request.values.get('id', 0, type=int)
    sensor = Sensor.query.filter_by(id=id).first()
    if sensor is not None:
        db.session.delete(sensor)
        return 'ok'
    else:
        return 'fail'