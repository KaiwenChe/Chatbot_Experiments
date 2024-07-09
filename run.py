# File path: run.py

from flask import Flask
from app.routes.chat_routes import chat_routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(chat_routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)