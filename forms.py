from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, 

# Set your Form classes below:

class GenerateForm(Form):
    name = TextField(
        'Text', validators=[DataRequired(), Length(min=2, max=40)]
    )