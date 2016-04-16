#-*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from . import sensor
from ..models import MainStation, SonModel, Sensor
from .forms import SonModelForm
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
        else:
            sonModel = SonModel(name=form.sonModelName.data,
                                location=form.location.data,
                                sensorsNumber=int(form.numSensor.data),
                                slaveaddress=int(form.slaveaddress.data)
                                )
            if not SonModel.setComNumber(int(form.parentModel.data)):
                flash('Setting Fail')
            db.session.add(sonModel)
            return redirect(url_for('sensor.display', count=int(form.numSensor.data) ))
    return render_template('createSonModel.html', form=form)


@sensor.route('/display/<count>', methods=['GET','POST'])
@login_required
def display(total):
    count = 0
    while count < total:
        sensor = Sensor(name='Sensor'+count, location='default', slave_id=sonModel.id)
        db.session.add(sensor)
        count += 1
    sensor = Sensor.query.all()
    return render_template('sensor/displaysensor.html',sensor=sensor)

