#-*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from . import sensor
from ..models import MainStation, SonModel, Sensor, SensorLog
from .forms import SonModelForm, SensorForm
from .. import db
from flask.ext.login import login_required
from ..decorators import admin_required, permission_required


@sensor.route('/createSonModel',methods=['GET', 'POST'])
@login_required
@admin_required
def createSonModel():
    form = SonModelForm()
    if form.validate_on_submit():
        if SonModel.query.filter_by(name=form.sonModelName.data).first():
            flash('This name is using.')
        elif SonModel.query.filter_by(slaveaddress=int(form.slaveaddress.data)).first():
            flash('This slaveaddress is using')
        else:
            sonmodel = SonModel(name=form.sonModelName.data,
                                location=form.location.data,
                                sensorsNumber=int(form.numSensor.data),
                                slaveaddress=int(form.slaveaddress.data)
                                )
            if not sonmodel.setComNumber(int(form.parentModel.data)):
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
                sensor = Sensor(name=sname, location='default', slave_id=s.id, position=2*count)
                db.session.add(sensor)
                count += 1
            db.session.add(s)
    sonmodels = SonModel.query.all()
    sensor = Sensor.query.all()
    slog = SensorLog.query.all()
    return render_template('displaysensor.html', sensor=sensor, sonmodels=sonmodels, sensorlog=slog)

@sensor.route('/createSensor/<id>', methods=['GET', 'POST'])
@login_required
def createSensor(id):
    form = SensorForm()
    if form.validate_on_submit():
        sensor = Sensor.query.filter_by(id=id).first()
        if sensor:
            sensor.name = form.sensorName.data
            sensor.location = form.location.data
            if not sensor.is_run:
                sensor.is_run = True
            db.session.add(sensor)
            return redirect(url_for('sensor.display'))
    return render_template('createSensor.html', form=form)

