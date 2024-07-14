// File: js/history.js
import { state } from './state.js';
import { formatDate } from './utils.js';
import { loadChat } from './chat.js';

export function toggleHistoryPanel() {
    state.isPanelOpen = !state.isPanelOpen;
    state.historyPanel.classList.toggle('open');
    state.toggleHistoryBtn.classList.toggle('open');
    
    if (state.isPanelOpen) {
        state.toggleHistoryBtn.style.left = '310px';
    } else {
        state.toggleHistoryBtn.style.left = '10px';
    }
}

export async function loadChatHistories() {
    try {
        const response = await fetch('/api/chat_histories');
        const histories = await response.json();
        state.historyList.innerHTML = '';
        histories.forEach(history => {
            const historyItem = document.createElement('div');
            historyItem.classList.add('history-item');
            if (history.chat_id === state.chatId) {
                historyItem.classList.add('active');
            }
            
            const dateElement = document.createElement('div');
            dateElement.classList.add('history-item-date');
            dateElement.textContent = formatDate(history.start_time);
            
            const previewElement = document.createElement('div');
            previewElement.classList.add('history-item-preview');
            previewElement.textContent = `${history.user_name} & ${history.assistant_name}`;
            
            historyItem.appendChild(dateElement);
            historyItem.appendChild(previewElement);
            
            historyItem.addEventListener('click', () => loadChat(history.chat_id));
            state.historyList.appendChild(historyItem);
        });
    } catch (error) {
        console.error('Error loading chat histories:', error);
    }
}