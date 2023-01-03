import openai
from flask import Flask, request, render_template, jsonify

# Set the API key
openai.api_key = "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"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get the text to generate an image for
    text = request.form.get('text')
    # Set the prompt for the image
    prompt = f"Write a description of the image you want to generate based on the following text: {text}"
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
