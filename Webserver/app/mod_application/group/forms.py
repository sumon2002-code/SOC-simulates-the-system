from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField, TextAreaField, SelectField

from utlis.forms import _get_fields
from utlis.dictionary import COLORs as COLORS

COLORs = COLORS()
class GroupForm(FlaskForm):
    title = StringField(description='Add Title',
                        validators=(DataRequired(), Length(1, 128)))
    
    description = TextAreaField(description='Add Description',
                                validators=(Length(0, 128),))
    
    color = SelectField(
        label='Select Group Color',
        choices=[
            (key, name)
            for key, name in COLORS.colors_bootstrap.items()
        ]
    )

    
    def get_fields(self):
        return _get_fields(self)
# End