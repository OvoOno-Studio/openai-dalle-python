from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

# Set your Form classes below:
class GenerateForm(FlaskForm):
    text = StringField('Text as description that will AI use to generate image:', validators=[DataRequired(), Length(min=2, max=40)])
    recaptcha = RecaptchaField()

class DonateForm(FlaskForm):
    wallet_address = StringField('Wallet Address', validators=[DataRequired(), Length(min=42, max=42), Regexp('^0x[a-fA-F0-9]{40}$', message='Enter a valid Ethereum address')])
    amount = DecimalField('Amount (Ether)', validators=[DataRequired()])
    submit = SubmitField('Donate')