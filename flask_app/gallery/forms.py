from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

class PostGalleryForm(FlaskForm):
    title = StringField('Title')
    gallery_picture = FileField('Upload Image', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    content = TextAreaField('About Paragraph')
    price = StringField('How much?')
    submit = SubmitField('Post')
