function sendCommand() {
    let inputField = document.getElementById('user-input');
    let command = inputField.value;
    if (command.trim() === "") return;

    // Append user message
    let userMessageBox = document.createElement('div');
    userMessageBox.classList.add('chat-box', 'user-box');
    let userMessage = document.createElement('div');
    userMessage.classList.add('message');
    userMessage.textContent = command;
    userMessageBox.appendChild(userMessage);
    document.getElementById('response-container').appendChild(userMessageBox);

    // Create typing animation box
    let responseContainer = document.getElementById('response-container');
    let typingBox = document.createElement('div');
    typingBox.classList.add('chat-box', 'generator-box');
    let typingMessage = document.createElement('div');
    typingMessage.classList.add('typing-container');
    typingMessage.textContent = "Generating...";
    typingBox.appendChild(typingMessage);
    responseContainer.appendChild(typingBox);
    responseContainer.scrollTop = responseContainer.scrollHeight; // Scroll to the bottom

    fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command: command })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing animation
            responseContainer.removeChild(typingBox);

            let messageBox = document.createElement('div');
            messageBox.classList.add('chat-box', 'generator-box');
            let message = document.createElement('div');
            message.classList.add('message');

            if (data.error) {
                message.textContent = data.error;
            } else {
                if (data.emails) {
                    message.innerHTML = `Emails: <br>${data.emails.join('<br>')}`;
                }
                if (data.passwords) {
                    if (data.emails) message.innerHTML += `<br><br>`;
                    message.innerHTML += `Passwords: <br>${data.passwords.join('<br>')}`;
                }
            }

            messageBox.appendChild(message);
            responseContainer.appendChild(messageBox);
            responseContainer.scrollTop = responseContainer.scrollHeight; // Scroll to the bottom
            inputField.value = "";
        });
}