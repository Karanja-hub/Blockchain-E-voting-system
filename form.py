from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from flask_wtf.csrf import CSRFProtect
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from models import User

csrf = CSRFProtect()

class Registration(FlaskForm):
  first_name = StringField(label="First Name", validators=[DataRequired()])
  last_name = StringField(label="Last Name", validators=[DataRequired()])
  age = IntegerField(label="Age", validators=[DataRequired()])
  email_address = StringField(label="Email Address", validators=[Email(), DataRequired()])
  phone_number = StringField(label="Phone number",validators=[Length(min=10, max=10, message="Invalid Phone Number"),DataRequired()])
  password = PasswordField(label="Password", validators=[Length(min=5, message="Password must be more than 5 characters"), DataRequired()])
  password1 = PasswordField(label="Confirm Password", validators=[EqualTo("password", message="Passwords do not match"), DataRequired()])

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = User.query.filter_by(phone=phone_number_to_validate.data).first()
    if phone_number:
      raise ValidationError("Phone Number already exists, Please try another one")

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = phone_number_to_validate.data
    if phone_number[0] != str(0):
      raise ValidationError("Invalid phone number. Phone number must begin with 0")
    elif phone_number[1] != str(7) and phone_number[1] != str(1):
      raise ValidationError("Invalid phone number. Phone number must begin with 0 followed by 7 or 1")

  def validate_email_address(self, email_to_validate):
    email = User.query.filter_by(email=email_to_validate.data).first()
    if email:
      raise ValidationError("Email Address already exists, Please try another one")
  
  def validate_age(self, age_to_validate):
    user_age = age_to_validate.data
    if user_age < 18:
      raise ValidationError("You're too young to be a registered voter")

class Login(FlaskForm):
  email_address = StringField(label="Email Address", validators=[DataRequired()])
  password = PasswordField(label="Password", validators=[DataRequired()])

class Verification(FlaskForm):
  secret_key = StringField(label="Enter Secret Key", validators=[DataRequired()])

class I_voted(FlaskForm):
  private_key = StringField(label="Enter Private Key", validators=[DataRequired()])
