const API_BASE = "http://127.0.0.1:8000";

document.getElementById("welcomeTime").textContent = formatTime(new Date());

function formatTime(date) {
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}