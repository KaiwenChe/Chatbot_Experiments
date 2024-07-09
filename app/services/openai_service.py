from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class OpenAIService:
    @staticmethod
    def generate_response(messages):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[msg for msg in messages if msg['role'] != 'system'] + [Config.SYSTEM_MESSAGE]
        )
        return response.choices[0].message.content