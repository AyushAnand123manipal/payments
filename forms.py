from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, TextAreaField, EmailField, SelectField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange, ValidationError, Regexp
from currency_service import get_supported_currencies
from models import User
import re

def validate_username(form, field):
    if not re.match(r"^[a-zA-Z0-9_]+$", field.data):
        raise ValidationError('Username can only contain letters, numbers, and underscores')

def validate_password(form, field):
    if len(field.data) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    if not re.search(r"[A-Z]", field.data):
        raise ValidationError('Password must contain at least one uppercase letter')
    if not re.search(r"[a-z]", field.data):
        raise ValidationError('Password must contain at least one lowercase letter')
    if not re.search(r"\d", field.data):
        raise ValidationError('Password must contain at least one number')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=64, message='Username must be between 3 and 64 characters'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must start with a letter and can only contain letters, numbers, dots or underscores')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email cannot exceed 120 characters')
    ])
    phone = StringField('Phone', validators=[
        Optional(),
        Length(min=10, max=15, message='Phone number must be between 10 and 15 digits'),
        Regexp(r'^\+?[0-9]{10,15}$', 0, 'Phone number must contain only numbers and an optional + prefix')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 0, 'Password must contain at least one uppercase letter, one lowercase letter, and one number')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(max=64, message='First name cannot exceed 64 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(max=64, message='Last name cannot exceed 64 characters')
    ])
    terms = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[
        DataRequired(message='You must agree to the terms and conditions')
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class SendMoneyForm(FlaskForm):
    recipient_email = StringField('Recipient Email', validators=[
        Optional(),
        Email(message='Please enter a valid email address'),
        Length(max=120)
    ])
    recipient_phone = StringField('Recipient Phone', validators=[
        Optional(),
        Length(min=10, max=15),
        Regexp(r'^\+?[0-9]+$', message='Phone number must contain only numbers and optional + prefix')
    ])
    amount = DecimalField('Amount', validators=[
        DataRequired(message='Amount is required'),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ], places=2)
    description = TextAreaField('Description (Optional)', validators=[
        Optional(),
        Length(max=200, message='Description must be less than 200 characters')
    ])
    submit = SubmitField('Send Money')

    def validate(self):
        if not super().validate():
            return False
        if not self.recipient_email.data and not self.recipient_phone.data:
            self.recipient_email.errors.append('Please provide at least an email or phone.')
            self.recipient_phone.errors.append('Please provide at least an email or phone.')
            return False
        return True

class AddMoneyForm(FlaskForm):
    amount = DecimalField('Amount', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ])
    source = SelectField('Source', choices=[
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI Payment'),
        ('wallet', 'Digital Wallet')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Money')

class ProfileUpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        Optional(),
        Length(max=50, message='First name cannot exceed 50 characters')
    ])
    last_name = StringField('Last Name', validators=[
        Optional(),
        Length(max=50, message='Last name cannot exceed 50 characters')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    preferred_currency = SelectField('Preferred Currency', choices=[
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('JPY', 'Japanese Yen (¥)'),
        ('INR', 'Indian Rupee (₹)'),
        ('CAD', 'Canadian Dollar (C$)'),
        ('AUD', 'Australian Dollar (A$)'),
        ('CNY', 'Chinese Yuan (¥)')
    ])
    submit = SubmitField('Update Profile')
    
class CurrencyConversionForm(FlaskForm):
    """Form for converting currency display in the dashboard."""
    currency = SelectField('Display Currency', choices=[
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('JPY', 'Japanese Yen (¥)'),
        ('INR', 'Indian Rupee (₹)'),
        ('CAD', 'Canadian Dollar (C$)'),
        ('AUD', 'Australian Dollar (A$)'),
        ('CNY', 'Chinese Yuan (¥)')
    ])
    submit = SubmitField('Change Currency')