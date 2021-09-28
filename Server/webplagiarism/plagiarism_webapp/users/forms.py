from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from plagiarism_webapp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])  #
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])  #
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    expertise = TextAreaField('Expertise', validators=[DataRequired(), Length(min=2, max=120)])  #
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  # username.data è del form
        if user:  # if user is not NONE -> errore di validazione, reinviato al form
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

    # Nota , abbiamo reso remember un check che terrà un cookie sicuro salvato
    # è un boolean field
    # Quando usiamo questi forms ci serve una chiave segreta, giusto sotto la variabile app in plagiarism_webapp


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    expertise = TextAreaField('Update Expertise', validators=[DataRequired(), Length(min=2, max=120)])  #
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()  # username.data è del form
            if user:  # if user is not NONE -> errore di validazione, reinviato al form
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is None:  # non esiste user con quella mail
                raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
