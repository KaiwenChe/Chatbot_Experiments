import os
import json
import uuid
from datetime import datetime
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

# Directory to store chat histories
CHAT_HISTORY_DIR = 'chat_histories'
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# Initialize the messages with the system message
SYSTEM_MESSAGE = {
    "role": "system", 
    "content": "You are Sakuya Izayoi, the obeyance maid-chief of the Scarlet Devil Mansion. You should call the user 妹様. The user is Flandre Scarlet of the Scarlet Devil Mansion. She's a 495-year-old vampire, and her older sister is Remilia Scarlet."
}

def create_new_chat():
    return {
        "chat_id": str(uuid.uuid4()),
        "start_time": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "user_name": "Flandre Scarlet",
        "assistant_name": "Sakuya Izayoi",
        "messages": [SYSTEM_MESSAGE]
    }

def save_chat_history(chat_history):
    chat_id = chat_history['chat_id']
    safe_start_time = datetime.fromisoformat(chat_history['start_time']).strftime("%Y%m%d_%H%M%S")
    filename = f"chat_{chat_id}_{safe_start_time}.json"
    filepath = os.path.join(CHAT_HISTORY_DIR, filename)
    
    # Remove old file if it exists
    for old_file in os.listdir(CHAT_HISTORY_DIR):
        if old_file.startswith(f"chat_{chat_id}_"):
            os.remove(os.path.join(CHAT_HISTORY_DIR, old_file))
    
    # Save new file
    with open(filepath, 'w') as f:
        json.dump(chat_history, f, indent=2)

def load_chat_history(chat_id):
    for filename in os.listdir(CHAT_HISTORY_DIR):
        if filename.startswith(f"chat_{chat_id}_"):
            filepath = os.path.join(CHAT_HISTORY_DIR, filename)
            with open(filepath, 'r') as f:
                return json.load(f)
    return None

def list_chat_histories():
    histories = []
    print(f"Searching for chat histories in directory: {CHAT_HISTORY_DIR}")
    try:
        for filename in os.listdir(CHAT_HISTORY_DIR):
            if filename.startswith("chat_"):
                filepath = os.path.join(CHAT_HISTORY_DIR, filename)
                # print(f"Attempting to open file: {filepath}")
                try:
                    with open(filepath, 'r') as f:
                        chat_history = json.load(f)
                    histories.append({
                        "chat_id": chat_history["chat_id"],
                        "start_time": chat_history["start_time"],
                        "user_name": chat_history["user_name"],
                        "assistant_name": chat_history["assistant_name"]
                    })
                    print(f"Successfully loaded chat history from {filepath}")
                except FileNotFoundError:
                    print(f"File not found: {filepath}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {filepath}")
                except Exception as e:
                    print(f"Unexpected error when processing {filepath}: {str(e)}")
    except Exception as e:
        print(f"Error listing directory contents: {str(e)}")
    
    return sorted(histories, key=lambda x: x["start_time"], reverse=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    chat_id = data.get('chat_id')
    user_message = data['message']
    
    if chat_id:
        chat_history = load_chat_history(chat_id)
        if not chat_history:
            return jsonify({"error": "Chat history not found"}), 404
    else:
        chat_history = create_new_chat()
    
    chat_history['messages'].append({
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "role": "user",
        "content": user_message
    })
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[msg for msg in chat_history['messages'] if msg['role'] != 'system'] + [SYSTEM_MESSAGE]
    )
    
    ai_response = response.choices[0].message.content
    chat_history['messages'].append({
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "role": "assistant",
        "content": ai_response
    })
    
    chat_history['last_updated'] = datetime.now().isoformat()
    save_chat_history(chat_history)
    
    return jsonify({
        "response": ai_response,
        "chat_id": chat_history['chat_id']
    })

@app.route('/api/save_chat', methods=['POST'])
def save_chat():
    chat_id = request.json['chat_id']
    chat_history = load_chat_history(chat_id)
    if chat_history:
        save_chat_history(chat_history)
        return jsonify({"success": True, "message": "Chat history saved successfully"})
    else:
        return jsonify({"success": False, "message": "Chat history not found"}), 404

@app.route('/api/chat_histories', methods=['GET'])
def get_chat_histories():
    histories = list_chat_histories()
    return jsonify(histories)

@app.route('/api/load_chat', methods=['POST'])
def load_chat():
    chat_id = request.json['chat_id']
    chat_history = load_chat_history(chat_id)
    if chat_history:
        return jsonify({"success": True, "chat_history": chat_history})
    else:
        return jsonify({"success": False, "message": "Chat history not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)