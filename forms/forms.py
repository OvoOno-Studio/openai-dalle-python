from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField
from wtforms.validators import DataRequired, Length

# Set your Form classes below:
class GenerateForm(FlaskForm):
    text = TextField('Text', validators=[DataRequired(), Length(min=2, max=40)])
    recaptcha = RecaptchaField()