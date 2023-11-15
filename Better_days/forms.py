from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

# 2 classes: one for Login and one for Register
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Email() ])
    password = PasswordField('Password', validators=[ DataRequired() ])
    submit = SubmitField('Sign In')

#Next class
class RegisterForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators=[ DataRequired() ])
    email = StringField('Email', validators=[ DataRequired(), Email() ])
    password = PasswordField('Password', validators=[ DataRequired() ])
    confirm_password = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')
