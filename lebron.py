import requests
import json

# API URL
url = "https://api.bfl.ai/v1/flux-pro-1.1"

# Payload to send in the request
payload = json.dumps({
  "prompt": "steph curry holding a happy valentines day sign",
  "width": 1024,
  "height": 768,
  "prompt_upsampling": False,
  "seed": 42,
  "safety_tolerance": 2,
  "output_format": "jpeg"
})

# Headers with API Key
headers = {
  'Content-Type': 'application/json',
  'X-Key': '76123e91-f7af-4beb-9aed-24c279ce4916'
}

# Making the POST request
response = requests.request("POST", url, headers=headers, data=payload)

# Display the result directly
if response.status_code == 200:
    print("Success:", response.json())  # Display the JSON response
else:
    print(f"Error: {response.status_code} - {response.text}")  # Error response
