# File path: run.py

from flask import Flask, render_template
from app.routes.chat_routes import chat_routes
from config import Config

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    app.register_blueprint(chat_routes)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)