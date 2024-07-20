// File: js/eventListeners.js
import { state } from './state.js';
import { sendMessage, startNewChat } from './chat.js';
import { toggleHistoryPanel, loadChatHistories, updateActiveChatInHistory } from './history.js';

export function setupEventListeners() {
    state.sendButton.addEventListener('click', sendMessage);
    state.userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    state.toggleHistoryBtn.addEventListener('click', toggleHistoryPanel);

    state.newChatBtn.addEventListener('click', () => {
        startNewChat();
        updateActiveChatInHistory(null);
    });

    window.addEventListener('focus', loadChatHistories);
}