from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from wtforms.fields.html5 import DateTimeLocalField
from todo.models import User

class SignupForm(FlaskForm):
    username = StringField(label="Username:", validators=[Length(min=3, max=60), DataRequired()])
    email_address = StringField(label="Email address:", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[Length(min=6), DataRequired()]) 
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label='Create Account')

    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data()).all()
        if user:
            raise ValidationError('Username is taken please try again.')

    def validate_email_address(self,email_to_validate):
        email = User.query.filter_by(email_address=email_to_validate.data()).all()
        if email:
            raise ValidationError('Email is already registered. Please try again')


        
class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Login")

class ToDoForm(FlaskForm):
    task = StringField(label="Task:", validators=[DataRequired(message="Please enter a task to complete")])
    due_date = DateTimeLocalField(label="Due date:", format="%Y-%m-%dT%H:%M", validators=[DataRequired(message="Please enter when you would like to complete task")])
    submit = SubmitField(label="Submit:")
