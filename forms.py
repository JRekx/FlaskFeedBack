from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm

class LoginF(FlaskForm):
    """
    Form for user login
    """
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=16)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=20)],
    )

class RegisterF(FlaskForm):
    """
    Form for user registration
    """
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=16)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=20)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=100)],
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=40)],
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=40)],
    )

class FeedbackF(FlaskForm):
    """
    Form for feedback submission
    """
    title = StringField(
        'Title',
        validators=[InputRequired(), Length(max=200)],
    )
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )

class DeleteF(FlaskForm):
    """
    Form for user deletion (if needed)
    """
    
    pass
