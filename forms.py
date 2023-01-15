from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, Length

# Set your Form classes below:
class GenerateForm(FlaskForm):
    name = TextField(
        'Text', validators=[DataRequired(), Length(min=2, max=40)]
    )

class DonateForm(FlaskForm):
    wallet_address = StringField('Wallet Address', validators=[DataRequired(), Length(min=42, max=42), Regexp('^0x[a-fA-F0-9]{40}$', message='Enter a valid Ethereum address')])
    amount = DecimalField('Amount (Ether)', validators=[DataRequired()])
    submit = SubmitField('Donate')