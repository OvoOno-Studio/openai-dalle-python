#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, request, send_from_directory, render_template, jsonify, flash 
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf.csrf import CSRFProtect
# from flask.ext.sqlalchemy import SQLAlchemy
from config import APIKey, dbPW, SecretKey 
from forms.forms import * 
import openai
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------# 

csrf = CSRFProtect()
openai.api_key = str(APIKey)  # Set the API key
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__) # Init app
# Application Configuration
app.config['SECRET_KEY'] = SecretKey # Secret Key
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB max-limit.
app.config['SERVER_NAME'] = 'dalle.emelrizvanovic.com'
app.config['SESSION_COOKIE_DOMAIN'] = False
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/uploads')

csrf.init_app(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/', methods=('GET', 'POST'))
def index():
    form = GenerateForm(request.form)
    donate_form = DonateForm(request.form)
    data = { 'form': 'generate-form', 'endpoint': '/generate', 'type': 'text/plain'}
    return render_template('pages/placeholder.home.html', form=form, donate_form=donate_form, data=data) 

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
def image_variations():
    form = VariationsForm(request.form)
    data = { 'form': 'variations-form', 'endpoint': '/image-variations', 'type': 'image/png'}
    return render_template('pages/placeholder.variations.html', form=form, data=data)

def image_variations(): 
    # form = VariationsForm(request.form)
    # if form.validate_on_submit():
    #     filename = photos.save(form.photo.data)
    #     file_url = photos.url(filename)
    # else:
    #     file_url = None
    photo = request.files['photo'] 

    if photo.content_length > 4*1024*1024:
        flash('Error: File size exceeds 4MB') 

    n = 1 # Number of images 
    size = "1024x1024" # Resolution of the new image
    # Generate the variation of the uploaded image
    response = openai.Image.create_variation(
        image=photo,
        n=n,
        size=size
    )
    # Return variation of the uploaded image 
    return jsonify({'url': response['data'][0]['url']})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsfot.icon')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)