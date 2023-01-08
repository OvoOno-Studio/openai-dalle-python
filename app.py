import openai 
from flask import Flask, request, render_template, jsonify
from config import APIKey
import urllib.request
import datetime

# Counts per IP
request_counts = {}

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
    # Get the user's IP
    user_ip = request.remote_addr

    # Check if the user's IP is in the dictionary
    if user_ip not in request_counts:
        # If not, add it and set the count to 1
        request_counts[user_ip] = {'count': 1, 'timestamp': datetime.datetime.now()}
    else:
        # If it is, increment the count
        request_counts[user_ip]['count'] += 1

    # Check if the user has made more than 5 requests today
    if request_counts[user_ip]['count'] > 5:
        # If they have, return an error message
        return jsonify({'error': 'You have exceeded the daily request limit.'})
        
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