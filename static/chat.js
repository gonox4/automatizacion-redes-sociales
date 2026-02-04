// --- AI Chat Logic ---

const chatWindow = document.getElementById('chat-window');
const chatBubble = document.getElementById('btn-open-chat');
const btnCloseChat = document.getElementById('btn-close-chat');
const chatInput = document.getElementById('chat-input');
const btnSendChat = document.getElementById('btn-send-chat');
const chatMessages = document.getElementById('chat-messages');

console.log("Chat system connected.");

chatBubble.addEventListener('click', () => {
    chatWindow.classList.remove('chat-closed');
    console.log("Chat opened");
});

btnCloseChat.addEventListener('click', () => {
    chatWindow.classList.add('chat-closed');
});

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    console.log("Sending message:", text);
    addMessage(text, 'user-msg');
    chatInput.value = '';

    const loadingMsg = addMessage("La IA está pensando...", 'ai-msg thinking');

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        console.log("AI Response:", data);
        
        if(loadingMsg && loadingMsg.parentNode) loadingMsg.remove();

        if (data.reply) {
            addMessage(data.reply, 'ai-msg');
        } else {
            addMessage("El Comandante no ha podido responder. Intenta de nuevo.", 'ai-msg');
        }

        if (data.actions && data.actions.length > 0) {
            if (window.fetchConfig) window.fetchConfig();
            if (window.fetchStats) window.fetchStats();
        }

    } catch (e) {
        console.error("Chat fetch error:", e);
        if(loadingMsg && loadingMsg.parentNode) loadingMsg.remove();
        addMessage("⚠️ Error de conexión. El servidor no responde.", 'ai-msg');
    }
}

function addMessage(text, className) {
    const div = document.createElement('div');
    div.className = `msg ${className}`;
    div.innerText = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
}

btnSendChat.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
