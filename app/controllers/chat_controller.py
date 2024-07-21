# File path: app/controllers/chat_controller.py

from app.models.chat import ChatTree
from app.services.openai_service import OpenAIService
from app.services.chat_history_service import ChatHistoryService

class ChatController:
    @staticmethod
    def process_message(user_message, chat_id=None):
        if chat_id:
            chat_tree = ChatHistoryService.load_chat_history(chat_id)
            if not chat_tree:
                return {"error": "Chat history not found"}, 404
        else:
            chat_tree = ChatTree("Flandre Scarlet", "Sakuya Izayoi")

        chat_tree.add_message(user_message, "user")

        # Use the stored current_branch instead of traversing the tree
        messages = [{"role": "system", "content": chat_tree.root.content}] + chat_tree.current_branch

        ai_response = OpenAIService.generate_response(messages)
        chat_tree.add_message(ai_response, "assistant")

        ChatHistoryService.save_chat_history(chat_tree)

        return {
            "response": ai_response,
            "chat_id": chat_tree.chat_id
        }

    @staticmethod
    def get_chat_histories():
        return ChatHistoryService.list_chat_histories()

    @staticmethod
    def load_chat(chat_id):
        chat_tree = ChatHistoryService.load_chat_history(chat_id)
        if chat_tree:
            return {"success": True, "chat_history": chat_tree.to_dict()}
        else:
            return {"success": False, "message": "Chat history not found"}, 404

    @staticmethod
    def delete_chat(chat_id):
        return ChatHistoryService.delete_chat_history(chat_id)