#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, request, redirect, url_for, render_template, jsonify 
# from flask.ext.sqlalchemy import SQLAlchemy
from config import APIKey, InfuraKey, dbPW, SecretKey 
from forms.forms import *
from web3 import Web3
import openai   

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# Counts per IP
request_counts = {}

# Connect to the Ethereum network using Infura
web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{InfuraKey}"))

# Set the API key
openai.api_key = str(APIKey)
app = Flask(__name__)
app.config['SECRET_KEY'] = SecretKey

@app.route('/', methods=('GET', 'POST'))
def index():   
    form = GenerateForm(request.form)
    donate_form = DonateForm(request.form)
    return render_template('pages/placeholder.home.html', form=form, donate_form=donate_form)

@app.route('/donate', methods=['POST'])
def donate():
    form = DonateForm() 

@app.route('/generate', methods=['POST', 'GET'])
def generate():
    # Get the text to generate an image for
    text = request.data
    # Set the prompt for the image 
    prompt = str(text)
    model = "image-alpha-001"
    num_images = 1
    size = "1024x1024"
    response_format = "url"
    # Generate the image
    response = openai.Image.create( 
        model=model,
        prompt=prompt,
        n=num_images,
        size=size,
        response_format=response_format 
    )   
    # Return the generated image URL to the client 
    return jsonify({'url': response['data'][0]['url']})

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)