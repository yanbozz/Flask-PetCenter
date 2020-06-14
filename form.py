from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError


class Length(object):
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = u'Field must be between %i and %i characters long.' % (min, max)
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            raise ValidationError(self.message)


class SignupForm(FlaskForm):
    '''use validators to verify the email address and password:
        1. Email(): check if valid email given
        2. InputRequired(): Sets the required attribute in the HTML
    '''
    full_name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=12)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo(
        'password', message="Passwords must match")])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')


class EditPetForm(FlaskForm):
    pet_name = StringField("Pet's Name", validators=[InputRequired()])
    pet_age = StringField("Pet's Age", validators=[InputRequired()])
    pet_bio = StringField("Pet's Bio", validators=[InputRequired()])
    submit = SubmitField('Edit Pet')


'''Reference:
    1. required attribute: https://www.w3schools.com/tags/att_input_required.asp
'''
