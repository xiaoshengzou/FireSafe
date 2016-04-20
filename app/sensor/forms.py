#-*- coding: utf-8 -*-

from flask.ext.wtf import Form 
from flask.ext.babel import gettext
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import Required, Length
from ..models import MainStation, SonModel, Sensor



class SonModelForm(Form):
    parentModel = SelectField('MainStation', coerce=int)
    sonModelName = StringField('Name', validators=[Required(), Length(1, 32)])
    slaveaddress = IntegerField('StationNO', validators=[Required()])
    location = StringField('Location', validators=[Required(), Length(1, 64)])
    numSensor = SelectField('Sensornum', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(SonModelForm, self).__init__(*args, **kwargs)
        self.numSensor.choices = [(x, x) for x in range(1,10)]
        self.parentModel.choices = [(model.id, model.portname)
                                     for model in MainStation.query.order_by(MainStation.name).all()]


class SensorForm(Form):
    sensorName = StringField('Name', validators=[Required(), Length(1, 32)])
    location = StringField('location', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Submit')
