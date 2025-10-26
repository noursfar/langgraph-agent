// ==================== Global State ====================
let currentSessionId = null;
let currentHrId = null;

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api/v1/pds';

// ==================== Page Navigation ====================
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

// ==================== Toast Notifications ====================
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    
    // Add icon based on type
    const icon = document.createElement('i');
    icon.className = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
    toast.insertBefore(icon, toast.firstChild);
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ==================== Loading Overlay ====================
function showLoading(message = 'Traitement en cours...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    loadingText.textContent = message;
    overlay.style.display = 'flex';
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'none';
}

// ==================== Error Display ====================
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
    
    setTimeout(() => {
        errorElement.style.display = 'none';
    }, 5000);
}

// ==================== Welcome Page ====================
document.getElementById('letsChatBtn').addEventListener('click', () => {
    showPage('initializePage');
});

document.getElementById('addDocsBtn').addEventListener('click', () => {
    showPage('documentsPage');
});

// ==================== Initialize Session ====================
document.getElementById('initializeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userId = document.getElementById('userId').value.trim();
    const token = document.getElementById('token').value.trim();
    
    if (!userId || !token) {
        showError('initError', 'Veuillez remplir tous les champs');
        return;
    }
    
    showLoading('Initialisation de la session...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/initialize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId, token }),
        });
        
        const data = await response.json();
        
        if (data.success && data.session_id) {
            currentSessionId = data.session_id;
            document.getElementById('sessionIdText').textContent = currentSessionId.substring(0, 8) + '...';
            showToast('Session initialisée avec succès !');
            showPage('chatPage');
            
            // Clear form
            document.getElementById('initializeForm').reset();
        } else {
            throw new Error(data.error || 'Échec de l\'initialisation de la session');
        }
    } catch (error) {
        console.error('Initialize error:', error);
        showError('initError', error.message);
        showToast('Échec de l\'initialisation de la session', 'error');
    } finally {
        hideLoading();
    }
});

// ==================== Back Buttons ====================
document.getElementById('backToWelcomeFromInit').addEventListener('click', () => {
    showPage('welcomePage');
});

document.getElementById('backToWelcomeFromChat').addEventListener('click', () => {
    if (confirm('Êtes-vous sûr de vouloir quitter la discussion ? Votre session sera perdue.')) {
        currentSessionId = null;
        showPage('welcomePage');
    }
});

document.getElementById('backToWelcomeFromDocs').addEventListener('click', () => {
    showPage('welcomePage');
    currentHrId = null;
});

// ==================== Chat Interface ====================
function addMessage(content, isUser = false) {
    const messagesContainer = document.getElementById('chatMessages');
    
    // Remove welcome message if it exists
    const welcomeMsg = messagesContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'agent'}`;
    
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="${isUser ? 'fas fa-user' : 'fas fa-robot'}"></i>
        </div>
        <div>
            <div class="message-content">
                <p>${content}</p>
            </div>
            <div class="message-time">${timeString}</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Auto-resize textarea
const messageInput = document.getElementById('messageInput');
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Handle Enter key in textarea
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.getElementById('chatForm').dispatchEvent(new Event('submit'));
    }
});

// Send message
document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    if (!currentSessionId) {
        showToast('Session non initialisée. Veuillez d\'abord initialiser.', 'error');
        showPage('initializePage');
        return;
    }
    
    // Add user message
    addMessage(message, true);
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Disable input
    const sendBtn = document.getElementById('sendBtn');
    messageInput.disabled = true;
    sendBtn.disabled = true;
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat/${currentSessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });
        
        const data = await response.json();
        
        hideTypingIndicator();
        
        if (data.success && data.response) {
            addMessage(data.response, false);
        } else {
            throw new Error(data.error || 'Échec de l\'obtention de la réponse');
        }
    } catch (error) {
        console.error('Chat error:', error);
        hideTypingIndicator();
        addMessage('Désolé, j\'ai rencontré une erreur. Veuillez réessayer.', false);
        showToast('Échec de l\'envoi du message', 'error');
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
});

// Clear chat
document.getElementById('clearChatBtn').addEventListener('click', () => {
    if (confirm('Êtes-vous sûr de vouloir effacer l\'historique de la discussion ?')) {
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.innerHTML = `
            <div class="welcome-message">
                <i class="fas fa-robot"></i>
                <p>Bonjour ! Je suis votre assistant IA. Comment puis-je vous aider aujourd'hui ?</p>
            </div>
        `;
        showToast('Discussion effacée');
    }
});

// ==================== Documents Management ====================

// Load documents for HR ID
document.getElementById('loadDocsBtn').addEventListener('click', async () => {
    const hrId = document.getElementById('hrId').value.trim();
    
    if (!hrId) {
        showToast('Veuillez entrer un HR ID', 'error');
        return;
    }
    
    currentHrId = hrId;
    showLoading('Chargement des documents...');
    
    try {
        await loadDocuments(hrId);
        document.getElementById('uploadSection').style.display = 'block';
        document.getElementById('documentsListSection').style.display = 'block';
        showToast('Documents chargés avec succès');
    } catch (error) {
        console.error('Load documents error:', error);
        showError('docsError', error.message);
        showToast('Échec du chargement des documents', 'error');
    } finally {
        hideLoading();
    }
});

async function loadDocuments(hrId) {
    try {
        const response = await fetch(`${API_BASE_URL}/documents/${hrId}`);
        const data = await response.json();
        
        if (data.success) {
            displayDocuments(data.documents || [], data.total_chunks || 0);
        } else {
            throw new Error(data.error || 'Échec du chargement des documents');
        }
    } catch (error) {
        throw error;
    }
}

function displayDocuments(documents, totalChunks) {
    const documentsList = document.getElementById('documentsList');
    const docsCount = document.getElementById('docsCount');
    
    docsCount.textContent = `${documents.length} document${documents.length !== 1 ? 's' : ''} (${totalChunks} fragments)`;
    
    if (documents.length === 0) {
        documentsList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-folder-open"></i>
                <p>Aucun document trouvé. Téléchargez votre premier document !</p>
            </div>
        `;
        return;
    }
    
    documentsList.innerHTML = documents.map(doc => `
        <div class="document-item" data-filename="${doc}">
            <div class="document-info">
                <div class="document-icon">
                    <i class="fas fa-file-pdf"></i>
                </div>
                <div class="document-details">
                    <h4>${doc}</h4>
                    <p>Document PDF</p>
                </div>
            </div>
            <button class="delete-doc-btn" onclick="deleteDocument('${doc}')">
                <i class="fas fa-trash"></i>
                Supprimer
            </button>
        </div>
    `).join('');
}

// File upload handling
const fileInput = document.getElementById('fileInput');
const fileNameDisplay = document.getElementById('fileNameDisplay');

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileNameDisplay.innerHTML = `<i class="fas fa-file-pdf"></i> ${file.name}`;
    }
});

// Drag and drop support
const fileUploadLabel = document.querySelector('.file-upload-label');

fileUploadLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadLabel.style.borderColor = 'var(--brand-color)';
    fileUploadLabel.style.background = 'var(--brand-color)';
});

fileUploadLabel.addEventListener('dragleave', () => {
    fileUploadLabel.style.borderColor = 'var(--brand-color)';
    fileUploadLabel.style.background = 'var(--bg-secondary)';
});

fileUploadLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadLabel.style.borderColor = 'var(--brand-color)';
    fileUploadLabel.style.background = 'var(--bg-secondary)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        fileNameDisplay.innerHTML = `<i class="fas fa-file-pdf"></i> ${files[0].name}`;
    }
});

// Upload document
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = fileInput.files[0];
    
    if (!file) {
        showToast('Veuillez sélectionner un fichier', 'error');
        return;
    }
    
    if (!currentHrId) {
        showToast('Veuillez d\'abord entrer et charger un HR ID', 'error');
        return;
    }
    
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showToast('Seuls les fichiers PDF sont autorisés', 'error');
        return;
    }
    
    showLoading('Téléchargement du document...');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('hrId', currentHrId);
        
        const response = await fetch(`${API_BASE_URL}/documents`, {
            method: 'POST',
            body: formData,
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(`Document téléchargé avec succès ! (${data.chunks_count} fragments)`);
            
            // Reset form
            document.getElementById('uploadForm').reset();
            fileNameDisplay.innerHTML = '<i class="fas fa-file-pdf"></i> Choisissez un fichier PDF ou glissez-le ici';
            
            // Reload documents
            await loadDocuments(currentHrId);
        } else {
            throw new Error(data.error || 'Échec du téléchargement du document');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError('docsError', error.message);
        showToast('Échec du téléchargement du document', 'error');
    } finally {
        hideLoading();
    }
});

// Delete document
async function deleteDocument(filename) {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer "${filename}" ?`)) {
        return;
    }
    
    if (!currentHrId) {
        showToast('HR ID non défini', 'error');
        return;
    }
    
    showLoading('Suppression du document...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/documents`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                hrId: currentHrId,
                filename: filename,
            }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Document supprimé avec succès');
            await loadDocuments(currentHrId);
        } else {
            throw new Error(data.error || 'Échec de la suppression du document');
        }
    } catch (error) {
        console.error('Delete error:', error);
        showError('docsError', error.message);
        showToast('Échec de la suppression du document', 'error');
    } finally {
        hideLoading();
    }
}

// Make deleteDocument available globally
window.deleteDocument = deleteDocument;

// ==================== Initialize App ====================
document.addEventListener('DOMContentLoaded', () => {
    // Show welcome page by default
    showPage('welcomePage');
    
    // Add smooth scroll behavior
    document.querySelectorAll('.chat-messages').forEach(el => {
        el.style.scrollBehavior = 'smooth';
    });
});
