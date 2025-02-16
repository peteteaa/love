from flask import Flask, render_template, request, jsonify, send_file
from lebron import generate_and_poll_image
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import tempfile

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch API_KEY from environment variables
API_KEY = os.getenv("API_KEY")

def add_recipient_name(image_url, recipient_name, from_name):
    # Download the image
    response = requests.get(image_url)
    original_img = Image.open(BytesIO(response.content))
    
    # Create a drawing object for text measurement
    temp_draw = ImageDraw.Draw(original_img)
    
    # Calculate initial font sizes
    base_font_size = int(min(original_img.width, original_img.height) * 0.05)
    to_font_size = int(base_font_size * 1.2)
    from_font_size = int(base_font_size * 1.1)
    
    # Use our readable font
    try:
        to_font = ImageFont.truetype("static/fonts/ComicNeue-Bold.ttf", to_font_size)
        from_font = ImageFont.truetype("static/fonts/ComicNeue-Bold.ttf", from_font_size)
    except:
        try:
            to_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", to_font_size)
            from_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", from_font_size)
        except:
            to_font = ImageFont.load_default()
            from_font = ImageFont.load_default()
    
    # Prepare text with heart emojis
    to_text = f"To: {recipient_name}"
    from_text = f"From: {from_name}"
    
    # Calculate text dimensions
    to_bbox = temp_draw.textbbox((0, 0), to_text, font=to_font)
    from_bbox = temp_draw.textbbox((0, 0), from_text, font=from_font)
    
    to_width = to_bbox[2] - to_bbox[0]
    to_height = to_bbox[3] - to_bbox[0]
    from_width = from_bbox[2] - from_bbox[0]
    from_height = from_bbox[3] - from_bbox[0]
    
    # Calculate required margin size based on text dimensions
    required_margin = max(
        int(to_width * 0.15),  # Extra 15% space for padding
        int(from_width * 0.15),
        int(to_height * 1.5),  # Extra space for vertical separation
        int(from_height * 1.5),
        int(min(original_img.width, original_img.height) * 0.06)  # Minimum margin size
    )
    
    # Create new image with calculated margins
    new_width = original_img.width + (required_margin * 2)
    new_height = original_img.height + (required_margin * 2)
    img = Image.new('RGB', (new_width, new_height), 'white')
    
    # Paste the original image in the center
    img.paste(original_img, (required_margin, required_margin))
    
    # Create drawing object for the new image
    draw = ImageDraw.Draw(img)
    
    # Calculate text positions
    padding = int(required_margin * 0.2)  # 20% of margin for padding
    to_x = required_margin + padding
    to_y = padding
    from_x = new_width - required_margin - from_width - padding
    from_y = new_height - from_height - padding
    
    def draw_text_with_shadow(x, y, text, font):
        # Draw multiple shadow layers for better visibility
        shadow_color = (0, 0, 0, 60)
        shadow_offset = int(font.size * 0.02)
        
        # Draw shadows
        for i in range(2):
            offset = shadow_offset * (i + 1)
            draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
        
        # Draw main text in a deep red
        draw.text((x, y), text, font=font, fill=(200, 30, 60, 255))
    
    # Draw both texts with shadows
    draw_text_with_shadow(to_x, to_y, to_text, to_font)
    draw_text_with_shadow(from_x, from_y, from_text, from_font)
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    img.save(temp_file.name, 'JPEG', quality=95)
    return temp_file.name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    recipient = data.get('recipient')
    
    if not prompt or not recipient:
        return jsonify({'error': 'Missing prompt or recipient name'}), 400
    
    try:
        # Get the celebrity name from the prompt (everything before "holding a Happy Valentine's Day sign")
        celebrity_name = prompt.split(" holding a Happy Valentine's Day sign")[0]
        
        # Generate image URL using the API key and prompt
        image_url = generate_and_poll_image(prompt, API_KEY)
        if not image_url:
            return jsonify({'error': 'Failed to generate image'}), 500
            
        # Add recipient name to the image
        processed_image_path = add_recipient_name(image_url, recipient, celebrity_name)
        
        # Serve the processed image
        return send_file(processed_image_path, mimetype='image/jpeg')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not API_KEY:
        print("Error: API key is missing. Ensure the .env file contains 'API_KEY'.")
    else:
        app.run(debug=True, port=5001)
