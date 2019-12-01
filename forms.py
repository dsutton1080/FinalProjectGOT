from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from constants import STATE_ABBREVS, STATE_NAMES, GRADE_LEVELS
from db_models import User, UserPost, ForumQuestion, ForumPost, Message, Follow


class LoginForm(FlaskForm):
    """
    This class inherits from the FlaskForm class in Flask. This defines the fields to be received in a Login POST request from the default page.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class PostForm(FlaskForm):
    content = StringField('Create a New Post', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Make Post')


class ForumQuestionForm(FlaskForm):
    question = StringField('Create a New Forum', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Create Forum')


# class MessageForm(FlaskForm):
#     message = StringField()
#     submit = SubmitField('Send')


class CommentForm(FlaskForm):
    comment = StringField(widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Add Comment')


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
    school = StringField('School')
    grade = SelectField('Grade in School', choices=GRADE_LEVELS, validators=[DataRequired()])
    state = SelectField('State', choices=list(zip(STATE_ABBREVS, STATE_NAMES)))
    submit = SubmitField('Join Now')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists.')


class SearchForm(FlaskForm):
    filt = SelectField('Search for other people!', choices=[('mentee', 'Mentee'), ('mentor', 'Mentor'), ('all', 'All Users')], validators=[DataRequired()])
    text = StringField('Search Input', validators=[DataRequired()])
    submit = SubmitField('Search')


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
