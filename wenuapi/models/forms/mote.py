from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField


class MoteForm(Form):
    level_id = IntegerField('Level ID', [validators.DataRequired()])
    mote_id = StringField('Mote ID', [validators.DataRequired()]) 
    resolution =StringField('Resolution', [validators.DataRequired()]) 
    x = IntegerField('X', [validators.DataRequired()])
    y = IntegerField('Y', [validators.DataRequired()])