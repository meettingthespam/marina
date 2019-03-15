from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError



### About Page Form ###

class AboutPageForm(FlaskForm):
    title = StringField('Title for About Page', validators=[DataRequired()])
    content = TextAreaField('Body of About Page', validators=[DataRequired()])
    submit = SubmitField('Post About Page')

### Home Page Form ###
class HomePageForm(FlaskForm):
    title = StringField('Title for Home Page', validators=[DataRequired()])
    content = TextAreaField('Body of Home Page', validators=[DataRequired()])
    main_photo = FileField('Main Background Photo', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post Home Page')


### CUSTOMER INQUIRY FORM ###

class CustomerMessageForm(FlaskForm):
    customer_name = StringField('Name', validators=[DataRequired("Please enter your name")])
    customer_email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email()])
    customer_phone = StringField('Phone Number', validators=[Length(min=7, max=15)])
    customer_message = TextAreaField('Message', validators=[DataRequired("Please enter your message")])
    customer_submit = SubmitField('Send Message')
