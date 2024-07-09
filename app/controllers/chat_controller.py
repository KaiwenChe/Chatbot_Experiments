# File path: app\controllers\chat_controller.py

from app.models.chat import ChatHistory
from app.services.openai_service import OpenAIService
from app.services.chat_history_service import ChatHistoryService

class ChatController:
    @staticmethod
    def process_message(user_message, chat_id=None):
        if chat_id:
            chat_history = ChatHistoryService.load_chat_history(chat_id)
            if not chat_history:
                return {"error": "Chat history not found"}, 404
        else:
            chat_history = ChatHistory("Flandre Scarlet", "Sakuya Izayoi")

        chat_history.add_message(user_message, "user")

        ai_response = OpenAIService.generate_response([msg.to_dict() for msg in chat_history.messages])
        chat_history.add_message(ai_response, "assistant")

        ChatHistoryService.save_chat_history(chat_history)

        return {
            "response": ai_response,
            "chat_id": chat_history.chat_id
        }

    @staticmethod
    def get_chat_histories():
        return ChatHistoryService.list_chat_histories()

    @staticmethod
    def load_chat(chat_id):
        chat_history = ChatHistoryService.load_chat_history(chat_id)
        if chat_history:
            return {"success": True, "chat_history": chat_history.to_dict()}
        else:
            return {"success": False, "message": "Chat history not found"}, 404