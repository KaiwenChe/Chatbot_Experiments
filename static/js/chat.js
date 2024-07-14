// File: js/chat.js
import { state } from './state.js';
import { addMessage } from './utils.js';
import { loadChatHistories } from './history.js';

export async function sendMessage() {
    const message = state.userInput.value.trim();
    if (message) {
        addMessage(message, true);
        state.userInput.value = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message, chat_id: state.chatId }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            addMessage(data.response, false);
            state.chatId = data.chat_id;
            
            await loadChatHistories();
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request.', false);
        }
    }
}

export async function loadChat(loadChatId) {
    try {
        const response = await fetch('/api/load_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chat_id: loadChatId }),
        });
        const data = await response.json();
        if (data.success) {
            state.chatId = data.chat_history.chat_id;
            state.chatMessages.innerHTML = '';
            data.chat_history.messages.forEach(msg => {
                if (msg.role !== 'system') {
                    addMessage(msg.content, msg.role === 'user');
                }
            });
            if (state.isPanelOpen) {
                toggleHistoryPanel();
            }
            loadChatHistories();
        } else {
            console.error('Failed to load chat:', data.message);
        }
    } catch (error) {
        console.error('Error loading chat:', error);
    }
}