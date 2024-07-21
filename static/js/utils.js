// File: js/utils.js
import { state } from './state.js';

export function addMessage(content, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    messageDiv.textContent = content;
    state.chatMessages.appendChild(messageDiv);
    state.chatMessages.scrollTop = state.chatMessages.scrollHeight;
}

export function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

export function renderChatTree(node) {
    if (node.role !== 'system') {
        addMessage(node.content, node.role === 'user');
    }
    node.children.forEach(child => renderChatTree(child));
}

export function flattenChatTree(node, messages = []) {
    if (node.role !== 'system') {
        messages.push({
            id: node.id,
            content: node.content,
            role: node.role,
            timestamp: node.timestamp
        });
    }
    node.children.forEach(child => flattenChatTree(child, messages));
    return messages;
}