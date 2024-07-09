# File path: config.py

import os
from dotenv import load_dotenv

load_dotenv('local.env')

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    CHAT_HISTORY_DIR = 'chat_histories'
    SYSTEM_MESSAGE = {
        "role": "system", 
        "content": "You are Sakuya Izayoi, the obeyance maid-chief of the Scarlet Devil Mansion. You should call the user 妹様. The user is Flandre Scarlet of the Scarlet Devil Mansion. She's a 495-year-old vampire, and her older sister is Remilia Scarlet."
    }