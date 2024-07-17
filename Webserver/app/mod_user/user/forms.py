import re

from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, BooleanField)
from wtforms.validators import (DataRequired, Email, EqualTo,
                                 Length, ValidationError)

from wtforms.widgets import PasswordInput
from utlis.forms import _get_fields

from app import bcrypt
from .models import User



class LoginForm(FlaskForm):
    email = StringField('Enter Your Email : ',
                        validators=(DataRequired(), Email()), description='email@gmail.com')
    
    password = PasswordField('Enter Your Password : ',
                             validators=(DataRequired(),), description='*'*8)
    remember = BooleanField('Remember', default=False)
    def validate_email(self, email):
        user = User.query.filter(User.email.ilike(f'{email.data}')).first()
        if (not user) or (not bcrypt.check_password_hash(user.password , self.password.data)) :
            raise ValidationError('The email or password is incorrect')
    
    def get_fields(self):
        return _get_fields(self)
# End

class RegisterForm(FlaskForm):
    full_name = StringField('Enter Your Full Name : ',
                            validators=(DataRequired(),), description='Full Name')
    email = StringField('Enter Your Email : ',
                        validators=(DataRequired(), Email()), description='email@gmail.com')
    password = PasswordField('Enter Your Password : ',
                             validators=(DataRequired(), Length(8,128)), description='*'*8)
    confirm_password = PasswordField(
        name='Confirm Your Password :',
        validators=(DataRequired(),
                    Length(8,128), EqualTo('password')), description='*'*8)
    
    def validate_email_(email):
        _ = User.query.filter(
                User.email.ilike(f'{email.date}'))
        if _:
            raise ValidationError('This Email Already Exists')
    
    def get_fields(self):
        return _get_fields(self)
# End

class SettingForm(FlaskForm):
    full_name = StringField('Your Full Name : ',
                        validators=(DataRequired(),), description='Full Name')
    email = StringField('Your Email : ',
                        validators=(DataRequired(), Email()), description='email@gmail.com')
    
    old_password = StringField('Enter Your Old Password : ',
                            validators=(DataRequired(), Length(8,128)),
                            widget=PasswordInput(hide_value=False))
    
    password = StringField('Enter Your New Password : ',
                            validators=(DataRequired(), Length(8,128)),
                            widget=PasswordInput(hide_value=False))
    
    confirm_password = StringField( name='Confirm Your New Password :',
                        validators=(DataRequired(), Length(8,128), EqualTo('password')),
                        widget=PasswordInput(hide_value=False))
# End    
    