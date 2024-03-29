from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, DecimalField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Regexp 

# GenerateForm class for generating AI images
class GenerateForm(FlaskForm):
    text = StringField('Text prompt:', validators=[DataRequired(), Length(min=2, max=200), Regexp(r'^[A-Za-z0-9]*$', message="Special characters are not allowed.")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Generate')
#DonateForm class for donating author in Etherum
class DonateForm(FlaskForm):
    wallet_address = StringField('Wallet Address', validators=[DataRequired(), Length(min=42, max=42), Regexp('^0x[a-fA-F0-9]{40}$', message='Enter a valid Ethereum address')])
    amount = DecimalField('Amount (Ether)', validators=[DataRequired()])
    submit = SubmitField('Donate')
#VariationsForm class for generating variations of uploaded image
class VariationsForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['png'], 'Only PNG allowed!')])
    submit = SubmitField('Generate')