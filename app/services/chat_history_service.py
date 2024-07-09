# File path: app\services\chat_history_service.py

import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from app.models.chat import ChatHistory
from config import Config

class ChatHistoryService:
    _executor = ThreadPoolExecutor(max_workers=4)

    @classmethod
    def save_chat_history(cls, chat_history):
        cls._executor.submit(cls._save_chat_history_async, chat_history)

    @staticmethod
    def _save_chat_history_async(chat_history):
        chat_id = chat_history.chat_id
        safe_start_time = datetime.fromisoformat(chat_history.start_time).strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{chat_id}_{safe_start_time}.json"
        filepath = os.path.join(Config.CHAT_HISTORY_DIR, filename)
        
        # Remove old file if it exists
        for old_file in os.listdir(Config.CHAT_HISTORY_DIR):
            if old_file.startswith(f"chat_{chat_id}_"):
                os.remove(os.path.join(Config.CHAT_HISTORY_DIR, old_file))
        
        # Save new file
        with open(filepath, 'w') as f:
            json.dump(chat_history.to_dict(), f, indent=2)

    @staticmethod
    def load_chat_history(chat_id):
        for filename in os.listdir(Config.CHAT_HISTORY_DIR):
            if filename.startswith(f"chat_{chat_id}_"):
                filepath = os.path.join(Config.CHAT_HISTORY_DIR, filename)
                with open(filepath, 'r') as f:
                    return ChatHistory.from_dict(json.load(f))
        return None

    @staticmethod
    def list_chat_histories():
        histories = []
        for filename in os.listdir(Config.CHAT_HISTORY_DIR):
            if filename.startswith("chat_"):
                filepath = os.path.join(Config.CHAT_HISTORY_DIR, filename)
                with open(filepath, 'r') as f:
                    chat_history = json.load(f)
                histories.append({
                    "chat_id": chat_history["chat_id"],
                    "start_time": chat_history["start_time"],
                    "user_name": chat_history["user_name"],
                    "assistant_name": chat_history["assistant_name"]
                })
        return sorted(histories, key=lambda x: x["start_time"], reverse=True)