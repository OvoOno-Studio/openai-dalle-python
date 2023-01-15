from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from wtforms.validators import DataRequired, Length

# Set your Form classes below:
class GenerateForm(FlaskForm):
    text = StringField('Text as description that will AI use to generate image:', validators=[DataRequired(), Length(min=2, max=40)])
    recaptcha = RecaptchaField()