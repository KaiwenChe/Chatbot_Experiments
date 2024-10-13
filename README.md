## 🌟 Overview

This project is a web-based chatbot application that serves as a practice implementation of features found in mainstream chatbot applications like ChatGPT. It's primarily designed as a learning exercise to understand and replicate key functionalities of modern AI-powered chat interfaces, with the following core functionalities:

1. A functional web-based chat interface
2. Integration with OpenAI's GPT-4o for generating responses
3. Chat history management (save, load, list, delete)
4. User interface for browsing and loading past chat sessions

While the chatbot currently role-plays as Sakuya Izayoi interacting with Flandre Scarlet (characters from the Touhou Project), this is mainly a placeholder to demonstrate user-assistant interactions. The core focus is on the technical implementation and functionality rather than the specific characters involved.

This project also serves as a potential platform for experimenting with additional features and concepts in AI-assisted conversations, such as:

- Implementing more advanced chat history management features like branching, re-structuring, and modification
- Exploring agentic workflows in AI conversations
- Testing novel interfaces like Claude Artifact and ChatGPT Canvas

As a practice project, it provides hands-on experience with full-stack development, API integration, and user interface design in the context of AI-powered applications.

## 🛠️ Technology Stack

- Backend: Python 3.12 with Flask
- Frontend: HTML, CSS, JavaScript (ES6 modules)
- AI Model: OpenAI GPT-4
- Environment Management: pipenv
- Configuration: python-dotenv for .env file handling

## 🔑 Key Features

1. Character-specific chatbot interactions
2. Web-based user interface for chatting
3. Integration with OpenAI's GPT-4 for generating responses
4. Chat history management (save, load, list, delete)
5. Asynchronous saving of chat sessions
6. User interface for browsing and loading past chat sessions
7. "New Chat" functionality to start fresh conversations
8. Thread-safe operations for chat history management

## 🚀 Setup Instructions

1. Ensure Python 3.12 is installed.
2. Install pipenv: `pip install pipenv`
3. Clone the repository and navigate to the project directory.
4. Install dependencies: `pipenv install`
5. Create a `local.env` file with your OpenAI API key: `OPENAI_API_KEY=your_key_here`

## 🏃‍♂️ Running the Application

1. Activate the pipenv shell: `pipenv shell`
2. Run the Flask application: `python run.py`
3. Open a web browser and go to `http://127.0.0.1:5000/`

## 📁 Project Structure

```
your_project/
├── app/
│   ├── controllers/
│   │   └── chat_controller.py
│   ├── models/
│   │   └── chat.py
│   ├── routes/
│   │   └── chat_routes.py
│   └── services/
│       ├── chat_history_service.py
│       └── openai_service.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── main.js
│       ├── chat.js
│       ├── history.js
│       ├── eventListeners.js
│       ├── state.js
│       └── utils.js
├── templates/
│   └── index.html
├── config.py
├── run.py
└── README.md
```

## 💻 Core Functionality

### Backend (app directory)

- Flask server handling API routes for chat interactions and history management
- MVC architecture with separate models, routes, controllers, and services
- Integration with OpenAI's API for generating chat responses
- Asynchronous saving of chat history using ThreadPoolExecutor
- Thread-safe operations for chat history management using read-write locks

### Frontend (static directory)

- Modular JavaScript structure using ES6 modules
- Simple state management system
- Separation of concerns: chat functionality, history management, event listeners, and utilities
- Responsive design for chat interface and history panel
- New Chat button for starting fresh conversations
- Delete functionality for removing specific chat histories

## 📊 Data Structure

Chat histories are stored as JSON files with the following structure:

```json
{
  "chat_id": "unique_identifier",
  "start_time": "ISO8601_timestamp",
  "last_updated": "ISO8601_timestamp",
  "user_name": "Flandre Scarlet",
  "assistant_name": "Sakuya Izayoi",
  "messages": [
    {
      "id": "message_unique_id",
      "timestamp": "ISO8601_timestamp",
      "role": "user" or "assistant",
      "content": "Message content"
    },
    // ... more messages
  ]
}
```

## 🔌 API Endpoints

1. `POST /api/chat`: Send a message and receive a response
2. `GET /api/chat_histories`: Retrieve a list of all chat histories
3. `POST /api/load_chat`: Load a specific chat history
4. `POST /api/delete_chat`: Delete a specific chat history

## 🆕 Recent Updates

- Implemented delete chat functionality
- Added a "New Chat" button to start fresh conversations
- Improved thread safety in the backend using read-write locks
- Fixed UI bug with chat history selection highlight
- Refactored frontend JavaScript for better state management and user interactions

## 🐛 Known Issues and Solutions

- File path issues on Windows: Resolved by using `os.path.join` for cross-platform compatibility
- Race conditions in chat history management: Resolved by implementing read-write locks

## 🔮 Future Improvements

- Implement user authentication
- Enhance the UI with character avatars and themed styling
- Add conversation branching or alternate history exploration
- Implement more advanced chat history management features

## 🔍 Troubleshooting

- If encountering issues with dependencies, try removing and reinstalling the virtual environment.
- Ensure the OpenAI API key is correctly set in the `local.env` file.
- Check the Flask server console for any error messages if the chatbot is not responding.
- If static files are not loading, check the browser console for 404 errors and verify file paths.

For any questions or issues, please contact the project maintainer.
