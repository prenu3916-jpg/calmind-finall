// script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const statusText = document.getElementById('status-text');

    // Function to add a message to the chat box
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        // Scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to send user input to the Flask API
    async function sendMessage() {
        const text = userInput.value.trim();
        if (text === '') return;

        // 1. Display user message and clear input
        addMessage(text, 'user');
        userInput.value = ''; 
        statusText.textContent = "Calmind is thinking...";
        sendButton.disabled = true;

        try {
            // 2. Call the Flask backend API
            const response = await fetch('/api/calmind', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                // Handle non-200 responses
                const errorData = await response.json().catch(() => ({response: "Server responded with an error."}));
                throw new Error(errorData.response || `HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            
            // 3. Display the AI's response
            const aiReply = data.response;
            const emotion = data.emotion;

            addMessage(aiReply, 'bot');
            statusText.textContent = `Emotion Detected: ${emotion.toUpperCase()}.`;
            
        } catch (error) {
            console.error('Error:', error);
            addMessage(error.message || "I am sorry, I couldn't connect to the AI service.", 'bot');
            statusText.textContent = "Error communicating with the server.";
        } finally {
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});