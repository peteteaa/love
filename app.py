from flask import Flask, render_template, request, jsonify
from lebron import generate_and_poll_image

app = Flask(__name__)
API_KEY = "76123e91-f7af-4beb-9aed-24c279ce4916"  # Your API key

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
        image_url = generate_and_poll_image(prompt, API_KEY)
        if image_url:
            return jsonify({'image_url': image_url})
        else:
            return jsonify({'error': 'Failed to generate image'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
