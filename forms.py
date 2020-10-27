from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    email = StringField("Email", [Email()])
    first_name = StringField("First Name", [InputRequired()])
    last_name = StringField("Last Name", [InputRequired()])
    

class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for adding feedback."""

    title = StringField("Title", [InputRequired()])
    content = TextAreaField("Content", [InputRequired()])