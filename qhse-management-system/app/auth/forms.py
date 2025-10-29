from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Employee','Employee'),('HSE Officer','HSE Officer'),('Supervisor','Supervisor')], default='Employee')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')  # this is the missing field
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    
class IncidentForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    department = SelectField("Department", choices=[("Administration","Administration"),("Production","Production"),("Quality Control","Quality Control"),("Field Operations","Field Operations")])
    type = SelectField("Type", choices=[("Near Miss","Near Miss"),("Spill","Spill"),("Injury","Injury"),("Fire","Fire")])
    date = DateField("Date", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit")
