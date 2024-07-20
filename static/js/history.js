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
            historyItem.dataset.chatId = history.chat_id;
            if (history.chat_id === state.chatId) {
                historyItem.classList.add('active');
            }
            
            const dateElement = document.createElement('div');
            dateElement.classList.add('history-item-date');
            dateElement.textContent = formatDate(history.start_time);
            
            const previewElement = document.createElement('div');
            previewElement.classList.add('history-item-preview');
            previewElement.textContent = `${history.user_name} & ${history.assistant_name}`;
            
            const deleteButton = document.createElement('button');
            deleteButton.classList.add('delete-chat-btn');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', (e) => {
                e.stopPropagation();
                deleteChat(history.chat_id);
            });
            
            historyItem.appendChild(dateElement);
            historyItem.appendChild(previewElement);
            historyItem.appendChild(deleteButton);
            
            historyItem.addEventListener('click', () => {
                selectChat(history.chat_id);
                loadChat(history.chat_id);
            });
            state.historyList.appendChild(historyItem);
        });
    } catch (error) {
        console.error('Error loading chat histories:', error);
    }
}

function selectChat(chatId) {
    // Remove 'active' class from all history items
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add 'active' class to the selected history item
    const selectedItem = document.querySelector(`.history-item[data-chat-id="${chatId}"]`);
    if (selectedItem) {
        selectedItem.classList.add('active');
    }
    
    state.chatId = chatId;
}

async function deleteChat(chatId) {
    if (confirm('Are you sure you want to delete this chat history?')) {
        try {
            const response = await fetch('/api/delete_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ chat_id: chatId }),
            });
            const data = await response.json();
            if (data.success) {
                if (state.chatId === chatId) {
                    state.chatId = null;
                    state.chatMessages.innerHTML = '';
                }
                loadChatHistories();
            } else {
                console.error('Failed to delete chat:', data.message);
            }
        } catch (error) {
            console.error('Error deleting chat:', error);
        }
    }
}

export function updateActiveChatInHistory(chatId) {
    selectChat(chatId);
}