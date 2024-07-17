from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import (StringField,
                        TextAreaField, SelectField)

from utlis.forms import _get_fields, MultiCheckboxField


class EventForm(FlaskForm):
    title = StringField(
        description='Title', name="eventTitle",
        validators=(DataRequired(), Length(1, 128)))
    
    url = StringField(
        description='URL Event', name="eventURL",
        validators=(Length(1, 128),))

    location = StringField(
        description='Location', name="eventLocation",
        validators=(Length(1, 128),))

    description = TextAreaField(
        description='Add Description',
        name="eventDescription",
        validators=(Length(1, 2048),))
    
    group = SelectField(
        label='Select The Task Group',
        name="eventLabel")

    start = SelectField(
        description='Start Time',
        validators=(DataRequired(),),
        name="eventStartDate") # Date And Time

    end =  SelectField(
        description='End Time',
        validators=(DataRequired(),),
        name="eventEndDate")  # Date And Time
    

    reminder = MultiCheckboxField(
        label='Reminder', name="eventReminder",
        description='Reminder Before The Event') 

    def get_fields(self):
        return _get_fields(self)
# End

def validate_event_form(data:dict)-> bool:
    """
    It confirms the validity of the
     event form (this form is sent to the 
     server through JavaScript in the file (calendar.js))
    """
    # --- Test 01 ---
    # Check for mandatory keys
    Keys = ['title', 'start', 'end']
    for key in Keys:
        if not data.get(key): return False
    # --- Test 01 --- #

    # --- Test 02 ---
    # Checking the validity of the data format (time-date)
    for key in (Keys[1], Keys[2]):
        # Possible error handling
        try:
            date, time = data.get(key).split(' ')
            hour, min = time.split(':')
            Y, M, D = date.split('-') 
        except ValueError:
            return False
        
        _pool = (hour, min, Y, M, D) # Data collection for Iterit
        for _ in _pool:
            try : int(_) # All values must be numeric data
            except ValueError: return False
    # --- Test 02 --- #

    # --- Test 03 ---
    # Checking the field (remembering)
    reminder = data.get('reminder') 
    if type(reminder) == list:
        for _ in reminder:
            try: int(_) # All values must be numeric data
            except ValueError: return False
        # If it is empty, something should happen (the form is valid)
    elif reminder == None: pass
    else: return False # No other format is acceptable
    # --- Test 03 --- #
    
    return True # The form is approved
# End


if __name__ == '__main__':
    data = {
        'title': 'Title Event',
        'start': '2024-1-2a8 18:00',
        'end': '2024-1-28 22:10'
    }

    print(
        validate_event_form(data)
    )