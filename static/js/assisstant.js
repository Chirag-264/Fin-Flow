document.addEventListener("DOMContentLoaded", function() {
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");

    chatForm.addEventListener("submit", function(event) {
        event.preventDefault();
        let userMessage = chatInput.value.trim();
        if (userMessage === "") return;

        // Append user message
        chatBox.innerHTML += `<div class="text-end"><b>You:</b> ${userMessage}</div>`;
        chatInput.value = "";

        // Fetch AI Response
        fetch("/ai-assistant", {
            method: "POST",
            body: JSON.stringify({ message: userMessage }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML += `<div><b>Assistant:</b> ${data.reply}</div>`;
        })
        .catch(error => console.error("Error:", error));
    });
});
