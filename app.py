import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory


# Load environment variables from local.env file
load_dotenv('local.env')

app = Flask(__name__)

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

# Initialize the messages with the system message
messages = [
    {"role": "system", "content": "You are Sakuya Izayoi, the obeyance maid-chief of the Scarlet Devil Mansion. You should call the user 妹様. The user is Flandre Scarlet of the Scarlet Devil Mansion. She's a 495-year-old vampire, and her older sister is Remilia Scarlet."}
]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global messages
    user_message = request.json['message']
    
    messages.append({"role": "user", "content": user_message})
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    ai_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_response})
    
    return jsonify({"response": ai_response})

if __name__ == '__main__':
    app.run(debug=True)