#-*- coding: utf-8 -*-

from flask.ext.wtf import Form 
from flask.ext.babel import gettext
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import Required, Length
from ..models import MainStation, SonModel, Sensor



class SonModelForm(Form):
    parentModel = SelectField(gettext('Station:'),coerce=int)
    sonModelName = StringField(gettext('Name:'), validators=[Required(), Length(1, 32)])
    slaveaddress = IntegerField(gettext('Slaveaddress:'), validators=[Required()])
    location = StringField(gettext('Location:'), validators=[Required(), Length(1, 64)])
    numSensor = SelectField(gettext('Sensornum:'), coerce=int)
    submit = SubmitField(gettext('Submit:'))

    def __init__(self, *args, **kwargs):
        super(SonModelForm, self).__init__(*args, **kwargs)
        self.numSensor.choices = [(x, x) for x in range(1,10)]
        self.parentModel.choices = [(model.id, model.portname)
                                     for model in MainStation.query.order_by(MainStation.name).all()]


# class SensorForm(Form):
#     grandModel = SelectField(u'所属主站',coerce=int)
#     parentModel = SelectField(u'所属从站', coerce=int)
#     sensorName = StringField('Name', validators=[Required(), Length(1, 32)])
#     location = StringField('location', validators=[Required(), Length(1, 64)])
#     explain = TextAreaField('explain')
#     port_id = IntegerField('port_id',validators=[Required()])
#     submit = SubmitField('Submit')

#     def __init__(self, *args, **kwargs):
#         super(SensorForm, self).__init__(*args, **kwargs)

#         self.grandModel.choices = [(model.id, model.mianModelName)
#                                      for model in MainModel.query.order_by(MainModel.mianModelName).all()]
#         self.parentModel.choices = [(sonModel.id, sonModel.sonModelName) for sonModel 
#                                     in SonModel.query.order_by(SonModel.sonModelName).all()]