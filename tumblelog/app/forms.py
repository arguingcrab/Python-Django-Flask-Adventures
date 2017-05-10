from flask_wtf import Form  
from wtforms import StringField, PasswordField  
from wtforms.validators import DataRequired


class LoginForm(Form):  
    """Login form to access writing and settings pages"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class RegisterForm(Form):  
    """Login form to access writing and settings pages"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class UserForm(Form):  
    """Login form to access writing and settings pages"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Verify Password', validators=[DataRequired()])