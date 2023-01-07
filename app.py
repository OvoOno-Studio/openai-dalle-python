import openai 
from flask import Flask, request, render_template, jsonify
from config import APIKey
import urllib.request

# Set the API key
openai.api_key = str(APIKey)

app = Flask(__name__) 

class Form:
    def __init__(self):
        self.text = ""

@app.route('/')
def index():
    return render_template('index.html') 


def save_image(image_url, save_path, image_name):
    """
    Save an image from a URL to a specified location on the server.
    
    Parameters:
    image_url (str): The URL of the image to be saved.
    save_path (str): The path to the location where the image will be saved (including the folder).
    image_name (str): The name to be given to the saved image.
    
    Returns:
    None
    """
    urllib.request.urlretrieve(image_url, f"{save_path}/{image_name}")

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

if __name__ == '__main__':
    app.run()