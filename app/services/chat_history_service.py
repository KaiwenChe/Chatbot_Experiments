# File path: app/services/chat_history_service.py

import os
import json
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from app.models.chat import ChatHistory
from config import Config

class ChatHistoryService:
    _executor = ThreadPoolExecutor(max_workers=4)
    _read_lock = threading.Lock()
    _write_lock = threading.Lock()

    @classmethod
    def save_chat_history(cls, chat_history):
        cls._executor.submit(cls._save_chat_history_async, chat_history)

    @classmethod
    def _save_chat_history_async(cls, chat_history):
        chat_id = chat_history.chat_id
        safe_start_time = datetime.fromisoformat(chat_history.start_time).strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{chat_id}_{safe_start_time}.json"
        
        os.makedirs(Config.CHAT_HISTORY_DIR, exist_ok=True)
        
        filepath = os.path.join(Config.CHAT_HISTORY_DIR, filename)
        
        with cls._write_lock:
            try:
                # Remove old file if it exists
                for old_file in os.listdir(Config.CHAT_HISTORY_DIR):
                    if old_file.startswith(f"chat_{chat_id}_"):
                        old_filepath = os.path.join(Config.CHAT_HISTORY_DIR, old_file)
                        if os.access(old_filepath, os.W_OK):
                            os.remove(old_filepath)
                        else:
                            print(f"Warning: Unable to remove old chat file {old_filepath} due to permissions.")
                
                # Save new file
                with open(filepath, 'w') as f:
                    json.dump(chat_history.to_dict(), f, indent=2)
            except PermissionError as e:
                print(f"Error: Unable to save chat history due to permission denied: {str(e)}")
            except Exception as e:
                print(f"Error: Unable to save chat history: {str(e)}")

    @classmethod
    def load_chat_history(cls, chat_id):
        os.makedirs(Config.CHAT_HISTORY_DIR, exist_ok=True)
        
        with cls._read_lock:
            for filename in os.listdir(Config.CHAT_HISTORY_DIR):
                if filename.startswith(f"chat_{chat_id}_"):
                    filepath = os.path.join(Config.CHAT_HISTORY_DIR, filename)
                    try:
                        with open(filepath, 'r') as f:
                            return ChatHistory.from_dict(json.load(f))
                    except PermissionError:
                        print(f"Warning: Unable to read chat history file {filename} due to permissions.")
                    except Exception as e:
                        print(f"Error reading chat history file {filename}: {str(e)}")
        return None

    @classmethod
    def list_chat_histories(cls):
        os.makedirs(Config.CHAT_HISTORY_DIR, exist_ok=True)
        
        histories = []
        with cls._read_lock:
            for filename in os.listdir(Config.CHAT_HISTORY_DIR):
                if filename.startswith("chat_"):
                    filepath = os.path.join(Config.CHAT_HISTORY_DIR, filename)
                    try:
                        if os.access(filepath, os.R_OK):
                            with open(filepath, 'r') as f:
                                chat_history = json.load(f)
                            histories.append({
                                "chat_id": chat_history["chat_id"],
                                "start_time": chat_history["start_time"],
                                "user_name": chat_history["user_name"],
                                "assistant_name": chat_history["assistant_name"]
                            })
                        else:
                            print(f"Warning: Unable to read chat history file {filename} due to permissions.")
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error reading chat history file {filename}: {str(e)}")
                    except Exception as e:
                        print(f"Unexpected error reading chat history file {filename}: {str(e)}")
        return sorted(histories, key=lambda x: x["start_time"], reverse=True)

    @classmethod
    def delete_chat_history(cls, chat_id):
        os.makedirs(Config.CHAT_HISTORY_DIR, exist_ok=True)
        
        with cls._write_lock:
            for filename in os.listdir(Config.CHAT_HISTORY_DIR):
                if filename.startswith(f"chat_{chat_id}_"):
                    filepath = os.path.join(Config.CHAT_HISTORY_DIR, filename)
                    try:
                        if os.access(filepath, os.W_OK):
                            os.remove(filepath)
                            return True
                        else:
                            print(f"Warning: Unable to delete chat history file {filename} due to permissions.")
                    except Exception as e:
                        print(f"Error deleting chat history file {filename}: {str(e)}")
        return False