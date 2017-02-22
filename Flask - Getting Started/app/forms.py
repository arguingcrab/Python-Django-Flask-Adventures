from flask_wtf import Form
from wtforms import StringField, BooleanField
# validator that checks that fields !empty
from wtforms.validators import DataRequired

# Have users login with OpenID
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)