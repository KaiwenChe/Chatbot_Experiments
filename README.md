# Sakuya Izayoi Chatbot Project

## Overview

This project is a web-based chatbot application that simulates conversations with Sakuya Izayoi, a character from the Touhou Project. The chatbot interacts with users as if they were Flandre Scarlet, another character from the same universe. The application uses OpenAI's GPT-4 for generating responses and includes functionality for saving, loading, and managing chat histories.

## Technology Stack

- Backend: Python 3.12 with Flask
- Frontend: HTML, CSS, JavaScript
- AI Model: OpenAI GPT-4
- Environment Management: pipenv
- Configuration: python-dotenv for .env file handling

## Key Features

1. Character-specific chatbot interactions
2. Web-based user interface for chatting
3. Integration with OpenAI's GPT-4 for generating responses
4. Chat history management (save, load, list)
5. Asynchronous saving of chat sessions
6. User interface for browsing and loading past chat sessions

## Setup Instructions

1. Ensure Python 3.12 is installed.
2. Install pipenv: `pip install pipenv`
3. Clone the repository and navigate to the project directory.
4. Install dependencies: `pipenv install`
5. Create a `local.env` file with your OpenAI API key: `OPENAI_API_KEY=your_key_here`

## Running the Application

1. Activate the pipenv shell: `pipenv shell`
2. Run the Flask application: `python run.py`
3. Open a web browser and go to `http://127.0.0.1:5000/`

## Core Functionality

### Backend (app directory)

- Flask server handling API routes for chat interactions and history management
- MVC architecture with separate models, routes, controllers, and services
- Integration with OpenAI's API for generating chat responses
- Asynchronous saving of chat history using ThreadPoolExecutor

### Frontend (index.html)

- Single-page application with chat interface and history panel
- JavaScript functions for sending/receiving messages, managing chat histories
- Ability to load previous chat sessions

## Data Structure

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

## API Endpoints

1. `POST /api/chat`: Send a message and receive a response
2. `GET /api/chat_histories`: Retrieve a list of all chat histories
3. `POST /api/load_chat`: Load a specific chat history

## Recent Updates

- Improved chat history loading in the frontend
- Added real-time updates of the chat history panel
- Implemented efficient chat history loading on page load and focus

## Known Issues and Solutions

- File path issues on Windows: Resolved by using `os.path.join` for cross-platform compatibility

## Future Improvements

- Implement user authentication
- Enhance the UI with character avatars and themed styling
- Add conversation branching or alternate history exploration
- Implement more advanced chat history management features

## Troubleshooting

- If encountering issues with dependencies, try removing and reinstalling the virtual environment.
- Ensure the OpenAI API key is correctly set in the `local.env` file.
- Check the Flask server console for any error messages if the chatbot is not responding.

For any questions or issues, please contact the project maintainer.