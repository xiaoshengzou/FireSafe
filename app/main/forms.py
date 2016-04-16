from flask.ext.wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length


class EditProfiledForm(Form):
        name = StringField('Real name', validators=[Length(0,64)])
        company = StringField('Company',validators=[Length(0,64)])
        submit = SubmitField('Submit')
