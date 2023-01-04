import openai 
from flask import Flask, request, render_template, jsonify
from config import APIKey
from PIL import Image, ImageDraw, ImageFont
import random, string

# Set the API key
openai.api_key = str(APIKey)

app = Flask(__name__)

# Dictionary to store the number of API requests made by each user
request_count = {}

class Form:
    def __init__(self):
        self.text = ""

@app.route('/')
def index():
    return render_template('index.html')
def form():
    # Generate a random CAPTCHA code and create an image for it
    captcha_code = ''.join([random.choice(string.ascii_uppercase + string.digits) for i in range(6)])
    image = create_captcha_image(captcha_code)
    
    # Save the image to a temporary file
    image.save('static/images/captcha.png')
    
    # Render the form template and pass the image URL to it
    return render_template('form.html', captcha_image_url='static/images/captcha.png')

def create_captcha_image(captcha_code):
    # Create an image with a white background
    image = Image.new('RGB', (200, 50), (255, 255, 255))
    
    # Create a draw object to draw on the image
    draw = ImageDraw.Draw(image)
    
    # Generate random positions and colors for the CAPTCHA code characters
    positions = [(random.randint(0, 200), random.randint(0, 50)) for i in range(6)]
    colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(6)]
    
    # Draw the CAPTCHA code characters on the image
    for i, c in enumerate(captcha_code):
        draw.text(positions[i], c, fill=colors[i])
    
    # Return the finished image
    return image

@app.route('/submit', methods=['POST'])
def submit():
    # Get the CAPTCHA code from the form submission
    captcha_code = request.form['captcha_code']
    
    # Check if the CAPTCHA code is correct
    if captcha_code == request.form['captcha_user_input']:
        # The CAPTCHA code is correct, process the form submission
        return "Form submission successful"
    else:
        # The CAPTCHA code is incorrect, show an error message
        return "Incorrect CAPTCHA code"

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