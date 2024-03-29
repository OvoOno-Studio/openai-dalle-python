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
app.config['SERVER_NAME'] = 'dalle-generator.ovoono.studio'
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
    num_images = 3 # change this to generate 3 images
    size = "1024x1024"
    response_format = "url" # Format of generated image
    # Generate the image
    response = openai.Image.create(  
        prompt=prompt,
        n=num_images,
        size=size,
        response_format=response_format 
    )   
    # Return the generated image URLs to the client 
    return jsonify({'urls': [data['url'] for data in response['data']]})  # changed this to return all urls

@app.route('/privacy')
def privacy():
    return render_template('pages/placeholder.privacy.html')

@app.route('/content-policy')
def policy():
    return render_template('pages/placeholder.content-policy.html')

@app.route('/variations', methods=['POST', 'GET'])
def variations():
    form = VariationsForm(request.form)
    data = { 'form': 'variations-form', 'endpoint': '/image-variations', 'type': 'application/json'}
    return render_template('pages/placeholder.variations.html', form=form, data=data)

@app.route('/image-variations', methods=['POST'])
def image_variations():  
    photo = request.files['photo'] 
    if not photo or not photo.filename:
        flash('Error: No photo selected')
        return
    # Check if image size is 1024x1024px
    if photo.content_length > 4*1024*1024:
        flash('Error: File size exceeds 4MB') 
        return
    #Check if image format is PNG
    if photo.content_type != 'image/png':
        flash('Error: File format is not PNG')
        return 
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


@app.route('/oauth/callback', methods=["POST", "GET"])
def oauth_callback():
    # handle the OAuth callback
    # Get the data passed in the request
    data = request.args.get("data") or "empty"
    # Log the data
    app.logger.info(f"Received ping request with data: {data}")
    # Return a JSON response to the external app
    return jsonify({f"message": data})

@app.route("/deauthorize", methods=["POST", "GET"])
def deauthorize():
    # Get the access token from the request
    access_token = request.form.get("access_token") or "empty"
    return jsonify({f"token": "{access_token}", "message": "Successfully deauthorized"})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsfot.icon')

@app.route('/robots.txt')
def robots_dot_txt():
    return "User-agent: * <br /> Disallow: /"

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)