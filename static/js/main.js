// File: js/main.js
import { loadChatHistories } from './history.js';
import { setupEventListeners } from './eventListeners.js';

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadChatHistories();
});