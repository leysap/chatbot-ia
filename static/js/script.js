function sendMessage() {
    let userInput = document.getElementById("user-input").value;

    if (userInput.trim() === "") return;

    // Mostrar el mensaje del usuario en el chat
    displayMessage(userInput, 'user');

    // Limpiar el input
    document.getElementById("user-input").value = "";

    // Llamar a la API de Flask para obtener la respuesta del chatbot
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            // Mostrar la respuesta de la IA
            displayMessage(data.response, 'ai');
        } else {
            displayMessage("Hubo un error al procesar tu mensaje.", 'ai');
        }
    })
    .catch(error => {
        console.error("Error:", error);
        displayMessage("Error al conectar con el servidor.", 'ai');
    });
}

function displayMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");

    messageElement.classList.add(sender);
    messageElement.innerText = message;

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

