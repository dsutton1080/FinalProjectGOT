from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms.fields.html5 import EmailField
from constants import STATE_ABBREVS, STATE_NAMES
from db_models import *


class LoginForm(FlaskForm):
    """
    This class inherits from the FlaskForm class in Flask. This defines the fields to be received in a Login POST request from the default page.
    """
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    """
    This class inherits from the FlaskForm class in Flask. This defines the fields to be received in a Login POST request from the Sign Up page.
    """
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username')
    email = EmailField('Email')
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            EqualTo('password_v', "Passwords must match."),
            Length(min=8)]
    )
    password_v = PasswordField('Verify Password')
    school = StringField('School')
    grade = SelectField('Grade in School', choices=[
        ('hs_fresh', 'High School Freshman'),
        ('hs_soph', 'High School Sophomore'),
        ('hs_jun', 'High School Junior'),
        ('hs_sen', 'High School Senior'),
        ('col_fresh', 'College Freshman'),
        ('col_soph', 'College Sophomore'),
        ('col_jun', 'College Junior'),
        ('col_sen', 'College Senior')
    ])
    state = SelectField('State', choices=list(zip(STATE_ABBREVS, STATE_NAMES)))
    submit = SubmitField('Join Now')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists.')

