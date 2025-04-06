document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const input = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");
  
    function appendMessage(sender, message) {
      const msg = document.createElement("div");
      msg.className = sender;
      msg.textContent = message;
      chatBox.appendChild(msg);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    async function sendMessage() {
      const userMessage = input.value.trim();
      if (!userMessage) return;
  
      appendMessage("user", userMessage);
      input.value = "";
  
      try {
        const response = await fetch("/nutrition/chatbot/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: JSON.stringify({ message: userMessage })
        });
  
        const data = await response.json();
        appendMessage("bot", data.response);
      } catch (error) {
        appendMessage("bot", "Sorry, something went wrong.");
      }
    }
  
    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keydown", e => {
      if (e.key === "Enter") sendMessage();
    });
    document.getElementById("reset-btn").addEventListener("click", async () => {
      try {
        const response = await fetch("/nutrition/chatbot/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: JSON.stringify({ message: "reset" })  // This is what triggers session flush in views.py
        });
    
        const data = await response.json();
        chatBox.innerHTML = "";
        appendMessage("bot", data.response);
      } catch (error) {
        appendMessage("bot", "Error restarting conversation.");
      }
    });
    
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
          const trimmed = cookie.trim();
          if (trimmed.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(trimmed.slice(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });

 