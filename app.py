from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key="AIzaSyDcAuUzekGauQQ6sv5_6JzRwB6Iq_9A_Yg")

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",  # Changed to pro version since flash might not be available
    generation_config=generation_config,
)

@app.route('/process', methods=['POST'])
def process_input():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({'error': 'No input provided in JSON'}), 400
        
        # Start chat session and send message
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(data['input'])
        
        # Return the response
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Server is running! Use the /process endpoint to interact."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)




