from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.fields.html5 import EmailField
from constants import STATE_ABBREVS, STATE_NAMES, GRADE_LEVELS
from db_models import *


class LoginForm(FlaskForm):
    """
    This class inherits from the FlaskForm class in Flask. This defines the fields to be received in a Login POST request from the default page.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    """
    This class inherits from the FlaskForm class in Flask. This defines the fields to be received in a Login POST request from the Sign Up page.
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            EqualTo('password_v', "Passwords must match."),
            Length(min=8)]
    )
    password_v = PasswordField('Verify Password', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    grade = SelectField('Grade in School', choices=GRADE_LEVELS, validators=[DataRequired()])
    state = SelectField('State', choices=list(zip(STATE_ABBREVS, STATE_NAMES)), validators=[DataRequired()])
    submit = SubmitField('Join Now')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists.')

class UpdateAccountForm(FlaskForm):
    """
    This class inherits from the FlaskForm class in Flask. This defines the fields to be received in a Login POST request from the Account page.
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password')
    new_password_v = PasswordField('Verify New Password')
    school = StringField('School', validators=[DataRequired()])
    grade = SelectField('Grade in School', choices=GRADE_LEVELS, validators=[DataRequired()])
    state = SelectField('State', choices=list(zip(STATE_ABBREVS, STATE_NAMES)), validators=[DataRequired()])
    submit = SubmitField('Update Account')