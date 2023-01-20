from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, DecimalField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Regexp
from flask_wtf.csrf import CSRFProtect

# GenerateForm class for generating AI images
class GenerateForm(FlaskForm):
    text = StringField('Image Description:', validators=[DataRequired(), Length(min=2, max=40)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Generate')
#DonateForm class for donating author in Etherum
class DonateForm(FlaskForm):
    wallet_address = StringField('Wallet Address', validators=[DataRequired(), Length(min=42, max=42), Regexp('^0x[a-fA-F0-9]{40}$', message='Enter a valid Ethereum address')])
    amount = DecimalField('Amount (Ether)', validators=[DataRequired()])
    submit = SubmitField('Donate')
#VariationsForm class for generating variations of uploaded image
class VariationsForm(FlaskForm):
    photo = FileField('Image', validators=[FileRequired(), FileAllowed(['png'], 'Only PNG allowed!')])
    submit = SubmitField('Generate')