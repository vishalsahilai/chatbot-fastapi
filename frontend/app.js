const API_BASE = "http://127.0.0.1:8000";

const typingIndicator = document.getElementById("typingIndicator");

document.getElementById("welcomeTime").textContent = formatTime(new Date());

function showTyping(show) {
  typingIndicator.style.display = show ? "flex" : "none";
  if (show) scrollToBottom();
}

function scrollToBottom() {
  setTimeout(() => {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }, 50);
}

function formatTime(date) {
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}