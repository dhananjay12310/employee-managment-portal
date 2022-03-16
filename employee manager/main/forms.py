from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField, SubmitField , IntegerField, DateField,  TextAreaField, EmailField ,RadioField , ValidationError

from wtforms.validators import Length , EqualTo , Email ,DataRequired
from main.models import emp_info , load_user

class  empRegForm(FlaskForm):


    def validate_email(self, email_to_check):
        email_address = emp_info.query.filter_by(email=email_to_check.data).first()

        if email_address:
            raise ValidationError('email address already exist! try a different email address')

    def validate_phone(self, phone_to_check):
        p = emp_info.query.filter_by(phone=phone_to_check.data).first()

        if p:
            raise ValidationError('phone number alredy exist! please try a different username')




    first_name = StringField(label='FIRST NAME:', validators=[Length(min=2,max=30), DataRequired()])
    last_name = StringField(label='LAST NAME:', validators=[Length(min=2,max=30), DataRequired()])
    email = EmailField(label='Email ADDRESS:', validators=[ Email() ,DataRequired()] )
    phone =StringField(label='Phone:',validators=[Length(min=10,max=10), DataRequired()])
    dob = DateField(label='DOB' , validators=[ DataRequired()])
    address = TextAreaField(label='ADDRESS:', validators=[Length(min=5), DataRequired()])
    password =PasswordField(label='Password:', validators=[Length(min=6),DataRequired()] )
    confirm_password =PasswordField(label='Confirm Pasword:', validators=[EqualTo('password'),DataRequired()] )
    admin = RadioField(label=' is Admin? :', choices=[(True,'YES'),(False,'No')], validators=[ DataRequired()])
    submit=SubmitField(label='CREATE ACCOUNT')


class admin_login_form(FlaskForm):
    email = StringField(label="Email:", validators=[ Email(), DataRequired()])
    password = PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='SIGN IN')

class employee_login_form(FlaskForm):
    email = StringField(label="Email:", validators=[ Email(), DataRequired()])
    password = PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='SIGN IN')




