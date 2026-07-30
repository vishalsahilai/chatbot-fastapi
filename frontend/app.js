const API_BASE = "http://127.0.0.1:8000";

// Session ID 
// Auto-generate and persist session_id in localStorage
function getSessionId() {
  let sid = localStorage.getItem("sadabahar_session_id");
  if (!sid) {
    sid = "user_" + crypto.randomUUID();
    localStorage.setItem("sadabahar_session_id", sid);
  }
  return sid;
}

const SESSION_ID = getSessionId();

// DOM References ──
const chatWindow     = document.getElementById("chatWindow");
const messageInput   = document.getElementById("messageInput");
const sendBtn        = document.getElementById("sendBtn");
const typingIndicator = document.getElementById("typingIndicator");
const suggestions    = document.getElementById("suggestions");

// Set welcome timestamp 
document.getElementById("welcomeTime").textContent = formatTime(new Date());

// Auto-resize textarea 
messageInput.addEventListener("input", () => {
  messageInput.style.height = "auto";
  messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + "px";
});

// Send on Enter (Shift+Enter for newline) 
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Send Message 
async function sendMessage() {
  const text = messageInput.value.trim();
  if (!text) return;

  // Hide suggestions after first message
  suggestions.style.display = "none";

  // Render user bubble
  appendMessage("user", text);

  // Clear input
  messageInput.value = "";
  messageInput.style.height = "auto";

  // Disable send button
  setLoading(true);

  // Show typing indicator
  showTyping(true);

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: SESSION_ID,
        message: text,
      }),
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || `Server error ${response.status}`);
    }

    const data = await response.json();
    showTyping(false);
    appendMessage("bot", data.response);

  } catch (error) {
    showTyping(false);
    appendErrorMessage(error.message);
  } finally {
    setLoading(false);
    messageInput.focus();
  }
}

// Send Suggestion ─
function sendSuggestion(btn) {
  // Extract text without emoji prefix
  const text = btn.textContent.replace(/^[^\s]+\s/, "").trim();
  messageInput.value = text;
  sendMessage();
}

// Append Message Bubble 
function appendMessage(role, text) {
  const isBot = role === "bot";

  const row = document.createElement("div");
  row.className = `msg-row ${isBot ? "bot-row" : "user-row"}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = isBot ? "S" : "U";

  const bubble = document.createElement("div");
  bubble.className = `bubble ${isBot ? "bot-bubble" : "user-bubble"}`;

  // Render text — support basic line breaks and bold (**text**)
  bubble.innerHTML = formatText(text);

  // Timestamp
  const ts = document.createElement("span");
  ts.className = "timestamp";
  ts.textContent = formatTime(new Date());
  bubble.appendChild(ts);

  row.appendChild(avatar);
  row.appendChild(bubble);

  chatWindow.appendChild(row);
  scrollToBottom();
}

// Append Error Bubble 
function appendErrorMessage(message) {
  const row = document.createElement("div");
  row.className = "msg-row bot-row";

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = "!";
  avatar.style.background = "#8B0000";

  const bubble = document.createElement("div");
  bubble.className = "bubble bot-bubble error-bubble";
  bubble.innerHTML = `⚠️ ${escapeHtml(message || "Something went wrong. Please try again.")}`;

  const ts = document.createElement("span");
  ts.className = "timestamp";
  ts.textContent = formatTime(new Date());
  bubble.appendChild(ts);

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatWindow.appendChild(row);
  scrollToBottom();
}

// Typing Indicator 
function showTyping(show) {
  typingIndicator.style.display = show ? "flex" : "none";
  if (show) scrollToBottom();
}

// Loading State
function setLoading(loading) {
  sendBtn.disabled = loading;
  messageInput.disabled = loading;
}

// Scroll to Bottom 
function scrollToBottom() {
  setTimeout(() => {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }, 50);
}

//Format Time 
function formatTime(date) {
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

// Format Text 
// Converts **bold**, newlines to HTML safely
function formatText(text) {
  let safe = escapeHtml(text);

  // Bold: **text** → <strong>text</strong>
  safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Newlines → <br>
  safe = safe.replace(/\n/g, "<br>");

  return safe;
}

//Escape HTML
function escapeHtml(text) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

// Focus input on load 
window.addEventListener("load", () => {
  messageInput.focus();
});