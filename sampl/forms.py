""" This module contains the flask form class definitions
"""
import re
import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from sampl import bcrypt
from sampl.models import User
from wtforms import (StringField, PasswordField,
        BooleanField, RadioField, SubmitField)
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    """ Defines the form entity for the registration page.
    """
    username = StringField(
            'Username',
            validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField(
            'Email',
            validators=[DataRequired(), Email()])
    date_of_birth = DateField(
            'Date of birth',
            validators=[DataRequired()], format="%Y-%m-%d", default=datetime.datetime.utcnow)
    password = PasswordField(
            'Password',
            validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
            'Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    show_password = BooleanField('Show Password')
    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        # Check for at least one lowercase letter
        if not re.search(r"[a-z]", password.data):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
        # Check for at least one uppercase letter
        if not re.search(r"[A-Z]", password.data):
            raise ValidationError("Password must contain at least one uppercase letter.")
        
        # Check for at least one digit
        if not re.search(r"\d", password.data):
            raise ValidationError("Password must contain at least one digit.")
        
        # Check for at least one special character
        if not re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password.data):
            raise ValidationError("Password must contain at least one special character.")
    
    
    def validate_username(self, username):
        # Check if username is taken
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        # Check if email is taken
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_date_of_birth(self, date_of_birth):
        # Checks for a legal and valid date of birth
        pass


class LoginForm(FlaskForm):
    """ Defines the form entity for the login page.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    """ Defines the form entity for User info update
    """
    new_username = StringField(
            'New Username',
            validators=[DataRequired(), Length(min=4, max=20)])
    new_email = StringField(
            'New Email',
            validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Update')
