from flask_wtf import Form  
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):  
    """Login form to access writing and settings pages"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class RegisterForm(Form):
    """Register form"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class UserForm(Form):
    """Edit user form"""
    email = StringField('Email', validators=[DataRequired()])
    active = BooleanField('Active')
    # status = StringField('Status', validators=[DataRequired()])
    password = PasswordField('Password')
    password2 = PasswordField('New Password')