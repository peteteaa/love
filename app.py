from flask import Flask, render_template, request, jsonify
from lebron import generate_and_poll_image
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch API_KEY from environment variables
API_KEY = os.getenv("API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        # Generate image URL using the API key and prompt
        image_url = generate_and_poll_image(prompt, API_KEY)
        if image_url:
            return jsonify({'image_url': image_url})
        else:
            return jsonify({'error': 'Failed to generate image'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not API_KEY:
        print("Error: API key is missing. Ensure the .env file contains 'API_KEY'.")
    else:
        app.run(debug=True)
