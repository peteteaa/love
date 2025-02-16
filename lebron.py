import requests
import time
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def generate_and_poll_image(prompt, api_key):
    # API URLs
    generate_url = "https://api.bfl.ai/v1/flux-pro-1.1-ultra"
    
    # Initial payload
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 768,
        "prompt_upsampling": False,
        "seed": random.randint(1,50),
        "safety_tolerance": 2,
        "output_format": "jpeg"
    }
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'X-Key': api_key
    }
    
    # Initial request to generate image
    response = requests.post(generate_url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error initiating generation: {response.status_code} - {response.text}")
        return None
    
    # Get polling URL from response
    try:
        response_data = response.json()
        polling_url = response_data.get('polling_url')
        
        if not polling_url:
            print("No polling URL found in response")
            return None
            
        print(f"Generation started. Polling URL: {polling_url}")

        # Poll the URL until the image is ready
        while True:
            poll_response = requests.get(polling_url)
            if poll_response.status_code == 200:
                poll_data = poll_response.json()
                if poll_data.get("status") == "Ready":
                    image_url = poll_data["result"]["sample"]
                    print(f"Image generated successfully: {image_url}")

                    return image_url
                else:
                    print("Image not ready yet, retrying in 3 seconds...")
                    time.sleep(3)
            else:
                print(f"Error polling: {poll_response.status_code} - {poll_response.text}")
                return None

    except Exception as e:
        print(f"Error during polling: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Fetch the API_KEY from environment variables
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("API key not found in .env file. Please ensure .env file contains 'API_KEY'.")
    else:
        s = input("Enter prompt for image generation: ")
        prompt = s + " holding a Happy Valentine's Day sign in a collage"
        
        final_image_url = generate_and_poll_image(prompt, api_key)
        
        if final_image_url:
            print(f"Final image URL: {final_image_url}")
            
            # Download the image
            image_response = requests.get(final_image_url)
            if image_response.status_code == 200:
                with open("generated_image.jpg", "wb") as f:
                    f.write(image_response.content)
                print("Image saved as 'generated_image.jpg'")
