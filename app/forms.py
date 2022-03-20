from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, FileField
from wtforms.validators import InputRequired, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

house_type = [('1','Apartment'),('2','house')]
class PropertyForm(FlaskForm):
    p_title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('PropertyDescription')
    location = StringField('location',validators=[DataRequired()])
    number_bedrooms= IntegerField('Number of bedrooms',validators=[DataRequired()])
    number_bathrooms= IntegerField('Number of bathrooms', validators=[DataRequired()])
    price = IntegerField('price',validators=[DataRequired()])
    property_type = SelectField('property type',choices=house_type)
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg','png','Images only!'])])