from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, Length, StringField, DecimalField, SubmitField

# Set your Form classes below:
class GenerateForm(Form):
    name = TextField(
        'Text', validators=[DataRequired(), Length(min=2, max=40)]
    )

class DonateForm(Form):
    wallet_address = StringField('Wallet Address', validators=[DataRequired(), Length(min=42, max=42), Regexp('^0x[a-fA-F0-9]{40}$', message='Enter a valid Ethereum address')])
    amount = DecimalField('Amount (Ether)', validators=[DataRequired()])
    submit = SubmitField('Donate')