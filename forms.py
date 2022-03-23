from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField)
from wtforms.validators import InputRequired, Length, Regexp

valid_search_time = "^(19[0-9][0-9]|20[0-9][0-9])(\/)(0[1-9]|1[0-2])(\/)(0[1-9]|1[0-9]|2[0-9]|3[0-1])\+(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$"

# The form rendered in the main-page with their corresponding validators
class PcapForm(FlaskForm):
    pcap_id = IntegerField('PCAP ID', validators=[InputRequired(message = "The PCAP ID must only consist of numbers")])
    device_name = StringField('Device Name',validators=[InputRequired(), Length(max=20)])
    session_id = IntegerField('Session ID', validators=[InputRequired(message = "The Session ID must only consist of numbers")])
    search_time = StringField('Search Time',validators=[InputRequired(), Length(max=30), Regexp(valid_search_time, message="The Search Time must have the format: yyyy/mm/dd+hr:min:sec")])
    submit = SubmitField('Submit')
    