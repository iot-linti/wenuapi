from wtforms import Form, StringField validators

class LevelForm(Form):
    map = StringField('Map', [validators.DataRequired()])