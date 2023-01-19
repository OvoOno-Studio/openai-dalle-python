#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, request, redirect, url_for, render_template, jsonify 
# from flask.ext.sqlalchemy import SQLAlchemy
from config import APIKey, dbPW, SecretKey 
from forms.forms import * 
import openai
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------# 

openai.api_key = str(APIKey)  # Set the API key
app = Flask(__name__)
app.config['SECRET_KEY'] = SecretKey # Secret Key
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB max-limit.

@app.route('/', methods=('GET', 'POST'))
def index():
    form = GenerateForm(request.form)
    donate_form = DonateForm(request.form)
    return render_template('pages/placeholder.home.html', form=form, donate_form=donate_form) 
 
@app.route('/generate', methods=['POST', 'GET'])
def generate(): 
    text = request.data # Get the text to generate an image for
    prompt = str(text) # Set the prompt for the image   
    num_images = 1
    size = "1024x1024"
    response_format = "url" # Format of generated image
    # Generate the image
    response = openai.Image.create(  
        prompt=prompt,
        n=num_images,
        size=size,
        response_format=response_format 
    )   
    # Return the generated image URL to the client 
    return jsonify({'url': response['data'][0]['url']})

@app.route('/image-variations', methods=['POST', 'GET'])
def index():
    form = VariationsForm(request.form)
    if form.validate_on_submit():
        assets_dir = os.path.join(
            os.path.dirname(app.instance_path), 'static/uploads'
        )
    return render_template('pages/placeholder.variations.html')

def generate_image_variations(): 
    image = request.data # Get the uploaded image  
    n = 1 # Number of images 
    size = "1024x1024" # Resolution of the new image
    # Generate the variation of the uploaded image
    response = openai.Image.create_variation(
        image=open(image, "rb"),
        n=n,
        size=size
    )
    # Return variation of the uploaded image 
    return jsonify({'url': response['data'][0]['url']})

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)