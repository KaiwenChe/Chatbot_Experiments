from flask import Blueprint, request, jsonify, send_from_directory
from app.controllers.chat_controller import ChatController

chat_routes = Blueprint('chat', __name__)

@chat_routes.route('/')
def index():
    return send_from_directory('.', 'index.html')

@chat_routes.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    chat_id = request.json.get('chat_id')
    result = ChatController.process_message(user_message, chat_id)
    return jsonify(result)

@chat_routes.route('/api/chat_histories', methods=['GET'])
def get_chat_histories():
    histories = ChatController.get_chat_histories()
    return jsonify(histories)

@chat_routes.route('/api/load_chat', methods=['POST'])
def load_chat():
    chat_id = request.json['chat_id']
    result = ChatController.load_chat(chat_id)
    return jsonify(result)