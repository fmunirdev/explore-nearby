from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from models import User


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired('Please enter your first name.')])
    last_name = StringField('Last Name', validators=[DataRequired('Please enter your last name.')])
    email = StringField('Email', validators=[DataRequired('Please enter your email address.'),
                                             Email('Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password.'),
                                                     Length(min=6, message='Passwords must be 6 characters or more.')])
    submit = SubmitField('Sign Up', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data).first()
        if user is not None:
            self.email.errors.append('Email is already taken.')
            return False

        self.user = user
        return True


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Please enter your email address.'),
                                             Email('Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password.'),
                                                     Length(min=6, message='Passwords must be 6 characters or more.')])
    submit = SubmitField('Sign Up', validators=[DataRequired()])


class AddressForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired('Please enter an address.')])
    submit = SubmitField('Search')