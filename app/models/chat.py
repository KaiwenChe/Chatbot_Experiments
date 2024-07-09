from datetime import datetime
import uuid

class Message:
    def __init__(self, content, role, timestamp=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.content = content
        self.role = role
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "role": self.role,
            "content": self.content
        }

class ChatHistory:
    def __init__(self, user_name, assistant_name, chat_id=None, start_time=None):
        self.chat_id = chat_id or str(uuid.uuid4())
        self.start_time = start_time or datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()
        self.user_name = user_name
        self.assistant_name = assistant_name
        self.messages = []

    def add_message(self, content, role):
        message = Message(content, role)
        self.messages.append(message)
        self.last_updated = datetime.now().isoformat()

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "start_time": self.start_time,
            "last_updated": self.last_updated,
            "user_name": self.user_name,
            "assistant_name": self.assistant_name,
            "messages": [msg.to_dict() for msg in self.messages]
        }

    @classmethod
    def from_dict(cls, data):
        chat = cls(
            user_name=data["user_name"],
            assistant_name=data["assistant_name"],
            chat_id=data["chat_id"],
            start_time=data["start_time"]
        )
        chat.last_updated = data["last_updated"]
        chat.messages = [Message(**msg) for msg in data["messages"]]
        return chat