// -- Navbar functions -- \\
function goHome() {
    // console.log("Go to home");
    window.location.href = "/";
}
// -- Profile functions -- \\
function toggleProfileDropdown() {
    console.log("Yoyoyo");
    const dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.classList.toggle("show");
}

// -- Chatbot functions -- \\
let isSending = false;
function toggleChatBox() {
    const chatbox = document.getElementById("chatbox");
    chatbox.classList.toggle("active");
}

function sendMessage() {
    const input = document.getElementById("chatbox-input");
    const message = input.value.trim();
    if (message && !isSending) {
        // Add user message to the chatbox
        const userMessage = document.createElement("div");
        userMessage.className = "message user-message";
        userMessage.textContent = message;
        document.getElementById("chatbox-messages").appendChild(userMessage);

        // Clear the input
        input.value = "";

        // Show loading message
        isSending = true;
        const loadingMessage = document.createElement("div");
        loadingMessage.className = "message bot-message loading-message";
        loadingMessage.textContent = "AI agent is typing";
        document
            .getElementById("chatbox-messages")
            .appendChild(loadingMessage);

        // Scroll to the bottom of the chatbox
        const chatboxMessages = document.getElementById("chatbox-messages");
        chatboxMessages.scrollTop = chatboxMessages.scrollHeight;

        // -- Response from AI agent -- \\

        // Get CSRF token
        const csrftoken = getCookie("csrftoken");

        // Send request to the server
        fetch("/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({ message: message }),
        })
            .then((response) => response.json())
            .then((data) => {
                // Remove the loading message
                isSending = false;
                loadingMessage.remove();

                // Add the bot's response
                const botMessage = document.createElement("div");
                botMessage.className = "message bot-message";
                botMessage.textContent = data.message;
                document
                    .getElementById("chatbox-messages")
                    .appendChild(botMessage);
            })
            .catch((error) => {
                // Remove the loading message
                isSending = false;
                loadingMessage.remove();

                // Add the bot's temperory response
                const tempMessage = document.createElement("div");
                tempMessage.className = "message bot-message";
                tempMessage.textContent =
                    "Something went wrong. Please try again!";
                document
                    .getElementById("chatbox-messages")
                    .appendChild(botMessage);
                setTimeout(() => {
                    // Remove the bot's temperory response
                    tempMessage.remove();
                }, 2000);

                console.error("Error:", error);
            });
    }
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}