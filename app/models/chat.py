# File path: app/models/chat.py

from datetime import datetime
import uuid

class ChatNode:
    def __init__(self, content, role, parent=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.content = content
        self.role = role
        self.timestamp = datetime.now().isoformat()
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "role": self.role,
            "content": self.content,
            "children": [child.to_dict() for child in self.children]
        }

class ChatTree:
    def __init__(self, user_name, assistant_name, chat_id=None, start_time=None):
        self.chat_id = chat_id or str(uuid.uuid4())
        self.start_time = start_time or datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()
        self.user_name = user_name
        self.assistant_name = assistant_name
        self.root = ChatNode("System message", "system")
        self.current_node = self.root
        self.current_branch = []  # Store the current branch of messages

    def add_message(self, content, role):
        new_node = ChatNode(content, role)
        self.current_node.add_child(new_node)
        self.current_node = new_node
        self.last_updated = datetime.now().isoformat()
        self.current_branch.append({"role": role, "content": content})  # Add to current branch

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "start_time": self.start_time,
            "last_updated": self.last_updated,
            "user_name": self.user_name,
            "assistant_name": self.assistant_name,
            "tree": self.root.to_dict(),
            "current_branch": self.current_branch
        }

    @classmethod
    def from_dict(cls, data):
        print("$$$$$$$$$$ DOING FROM DICT $$$$$$$$$$")
        chat_tree = cls(
            user_name=data["user_name"],
            assistant_name=data["assistant_name"],
            chat_id=data["chat_id"],
            start_time=data["start_time"]
        )
        chat_tree.last_updated = data["last_updated"]
        chat_tree.current_branch = data["current_branch"]
        cls._build_tree(chat_tree.root, data["tree"]["children"])
        # Set the current_node to the last node in the tree
        chat_tree.current_node = chat_tree._get_last_node(chat_tree.root)
        return chat_tree

    @classmethod
    def _build_tree(cls, parent, children_data):
        for child_data in children_data:
            child = ChatNode(child_data["content"], child_data["role"], id=child_data["id"])
            parent.add_child(child)
            cls._build_tree(child, child_data["children"])

    def _get_last_node(self, node):
        if not node.children:
            return node
        return self._get_last_node(node.children[-1])