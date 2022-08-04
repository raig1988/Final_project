from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, NumberRange
from budgetapp.models import User

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    password = PasswordField(label='Password', validators=[DataRequired(),Length(min=3)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username not available. Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email is used. Please choose another.')

class LoginForm(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    password = PasswordField(label='Password', validators=[DataRequired(),Length(min=3)])
    remember =  BooleanField('Remember Me')
    submit = SubmitField(label='Login')

class UpdateAccountForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    submit = SubmitField(label='Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username not available. Please choose another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email is used. Please choose another.')

class RequestResetForm(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    submit = SubmitField(label='Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired(),Length(min=3)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Reset Password')

class TransactionForm(FlaskForm):
    day = IntegerField("Day", validators=[DataRequired(),NumberRange(min=1, max=31)])
    month = IntegerField("Month", validators=[DataRequired(),NumberRange(min=1, max=12)])
    year = IntegerField("Year", validators=[DataRequired(),NumberRange(min=2000, max=3000)])
    type = SelectField("Type", choices=[('Apps'), ('Rent'), ('Services'), ('Groceries'), ('Cleaning'), ('Personal Care'), ('Supplements'), ('Health & Insurance'), ('Travel'), ('Others')], validators=[DataRequired()])
    expense = StringField("Expense", validators=[DataRequired()])
    amount= FloatField("Amount", validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField(label='Register Transaction')