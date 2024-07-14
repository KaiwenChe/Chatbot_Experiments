// File: js/eventListeners.js
import { state } from './state.js';
import { sendMessage } from './chat.js';
import { toggleHistoryPanel, loadChatHistories } from './history.js';

export function setupEventListeners() {
    state.sendButton.addEventListener('click', sendMessage);
    state.userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    state.toggleHistoryBtn.addEventListener('click', toggleHistoryPanel);

    window.addEventListener('focus', loadChatHistories);
}