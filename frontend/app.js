const API_BASE = "http://127.0.0.1:8000";

let isLoading = false;

function getSessionId() {
  let sid = localStorage.getItem("sadabahar_session_id");
  if (!sid) {
    sid = "user_" + crypto.randomUUID();
    localStorage.setItem("sadabahar_session_id", sid);
  }
  return sid;
}

const SESSION_ID = getSessionId();

const chatWindow      = document.getElementById("chatWindow");
const messageInput    = document.getElementById("messageInput");
const sendBtn         = document.getElementById("sendBtn");
const typingIndicator = document.getElementById("typingIndicator");
const suggestions     = document.getElementById("suggestions");

document.getElementById("welcomeTime").textContent = formatTime(new Date());

messageInput.addEventListener("input", () => {
  messageInput.style.height = "auto";
  messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + "px";
});

messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

async function sendMessage() {
  if (isLoading) return;
  const text = messageInput.value.trim();
  if (!text) return;

  suggestions.style.display = "none";
  appendMessage("user", text);
  messageInput.value = "";
  messageInput.style.height = "auto";
  setLoading(true);
  showTyping(true);

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: SESSION_ID, message: text }),
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

function sendSuggestion(btn) {
  const text = btn.textContent.replace(/^[^\s]+\s/, "").trim();
  messageInput.value = text;
  sendMessage();
}

function appendMessage(role, text) {
  const isBot = role === "bot";

  const row = document.createElement("div");
  row.className = `msg-row ${isBot ? "bot-row" : "user-row"}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = isBot ? "S" : "U";

  const bubble = document.createElement("div");
  bubble.className = `bubble ${isBot ? "bot-bubble" : "user-bubble"}`;
  bubble.innerHTML = formatText(text);

  const ts = document.createElement("span");
  ts.className = "timestamp";
  ts.textContent = formatTime(new Date());
  bubble.appendChild(ts);

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatWindow.appendChild(row);
  scrollToBottom();
}

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

function showTyping(show) {
  typingIndicator.style.display = show ? "flex" : "none";
  if (show) scrollToBottom();
}

function setLoading(loading) {
  isLoading = loading;
  sendBtn.disabled = loading;
  messageInput.disabled = loading;
}

function scrollToBottom() {
  setTimeout(() => {
    const last = chatWindow.lastElementChild;
    if (last) last.scrollIntoView({ behavior: "smooth", block: "end" });
  }, 50);
}

function formatTime(date) {
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

function formatText(text) {
  let safe = escapeHtml(text);
  safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  safe = safe.replace(/\n/g, "<br>");
  return safe;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

window.addEventListener("load", () => {
  messageInput.focus();
});