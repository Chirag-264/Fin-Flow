document.addEventListener("DOMContentLoaded", function () {
    console.log("FinFlow Loaded Successfully!");

    // Handle form submissions for login & registration
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            handleFormSubmission(form);
        });
    });

    // Initialize AI Assistant if present
    if (document.getElementById("chatbox")) {
        initializeChatbot();
    }
});

// ✅ Function to handle form submissions
function handleFormSubmission(form) {
    const formData = new FormData(form);
    fetch(form.action, {
        method: form.method,
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect || "/";
        } else {
            alert(data.message || "Something went wrong!");
        }
    })
    .catch(error => console.error("Error:", error));
}

// ✅ Function to initialize the AI Assistant Chat
function initializeChatbot() {
    const chatbox = document.getElementById("chatbox");
    const inputBox = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");

    sendBtn.addEventListener("click", function () {
        sendMessage(inputBox.value);
    });

    inputBox.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage(inputBox.value);
        }
    });

    function sendMessage(message) {
        if (!message.trim()) return;
        
        appendMessage("user", message);
        inputBox.value = "";

        fetch("/api/assistant", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => appendMessage("assistant", data.reply))
        .catch(error => console.error("Error:", error));
    }

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", sender);
        messageDiv.textContent = message;
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}

// ✅ Function to update rewards dynamically
function updateRewards(points) {
    const rewardDisplay = document.getElementById("reward-points");
    if (rewardDisplay) {
        rewardDisplay.textContent = `Points: ${points}`;
    }
}

// ✅ Function to fetch real-time stock data (Alpha Vantage API)
function fetchStockData(symbol) {
    fetch(`/api/market?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            const stockPrice = document.getElementById("stock-price");
            if (stockPrice) {
                stockPrice.textContent = `Stock Price: $${data.price}`;
            }
        })
        .catch(error => console.error("Error fetching stock data:", error));
}
