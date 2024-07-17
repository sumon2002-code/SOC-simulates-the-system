from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField, TextAreaField, SelectField, DateField

from utlis.forms import _get_fields, MultiCheckboxField


class TaskForm(FlaskForm):
    title = StringField(description='Add Title :',
                        validators=(DataRequired(), Length(1, 128)))
    
    description = TextAreaField(description='Add Description',
                                validators=(Length(0, 2048),))
    
    group = SelectField(label='Select The Task Group')

    deadline = DateField(description='Deadline Time',
            format='%Y-%m-%d', validators=(DataRequired(),))

    def get_fields(self):
        return _get_fields(self)
# ---