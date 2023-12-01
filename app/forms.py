from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo

class SignUpForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])
    confirm_pass=PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])
    submit=SubmitField('Log In')

class KanjiSearchForm(FlaskForm):
    meaning=StringField('Meaning')
    name_reading=StringField('Name Reading')
    kunyomi=StringField('Kunyomi Reading')
    onyomi=StringField('Onyomi Reading')
    submit=SubmitField('Search')