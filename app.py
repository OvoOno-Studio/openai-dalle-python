import openai 
from flask import Flask, request, render_template, jsonify
from config import APIKey 

# Set the API key
openai.api_key = str(APIKey)

app = Flask(__name__)

class Form:
    def __init__(self):
        self.text = ""

@app.route('/')
def index():
    return render_template('index.html')

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