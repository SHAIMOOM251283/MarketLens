// script.js
let currentFile = null;

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadSection = document.getElementById('upload-section');
const chatSection = document.getElementById('chat-section');
const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const loadingOverlay = document.getElementById('loading-overlay');
const loadingText = document.getElementById('loading-text');

// ===================== FILE UPLOAD =====================

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    handleFile(e.target.files[0]);
  }
});

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('border-cyan-500');
});

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('border-cyan-500');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('border-cyan-500');
  if (e.dataTransfer.files.length > 0) {
    handleFile(e.dataTransfer.files[0]);
  }
});

async function handleFile(file) {
  if (!file.name.endsWith('.json')) {
    alert("Please upload a JSON file");
    return;
  }

  // Show fullscreen loading overlay
  showLoading("Processing your file...");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch('/upload', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    hideLoading();

    if (data.error) {
      addMessage("bot", `❌ ${data.error}`);
      return;
    }

    currentFile = file.name;

    document.getElementById('file-info').innerHTML = `
      <p class="font-medium text-white">${file.name}</p>
      <p class="text-xs text-gray-500">Loaded successfully</p>
    `;

    uploadSection.classList.add('hidden');
    chatSection.classList.remove('hidden');

    addMessage("system", `✅ Successfully loaded <strong>${file.name}</strong>. Ask me anything about the products!`);

  } catch (err) {
    hideLoading();
    addMessage("bot", "❌ Upload failed. Please try again.");
  }
}

// ===================== LOADING OVERLAY =====================

function showLoading(message = "Processing your data...") {
  loadingText.textContent = message;
  loadingOverlay.classList.remove('hidden');
  // Optional: disable background interactions
  document.body.style.overflow = 'hidden';
}

function hideLoading() {
  loadingOverlay.classList.add('hidden');
  document.body.style.overflow = 'visible';
}

// ===================== RESPONSE FORMATTING =====================

function formatResponse(text) {
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  const lines = text.split("\n").map(line => line.trim());
  const isBulletList = lines.filter(l => l.startsWith("•")).length > 1;

  if (isBulletList) {
    return "<ul style='padding-left:20px; list-style-type: disc;'>" +
      lines
        .filter(l => l)
        .map(l => `<li>${l.replace(/^•\s*/, "")}</li>`)
        .join("") +
      "</ul>";
  }

  return text.replace(/\n/g, "<br>");
}

// ===================== CHAT =====================

function addMessage(sender, text) {
  const div = document.createElement('div');
  div.className = `chat-bubble ${sender === 'user' ? 'user-bubble' : 'bot-bubble'}`;

  div.innerHTML = formatResponse(text);

  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage() {
  const question = userInput.value.trim();
  if (!question) return;

  addMessage('user', question);
  userInput.value = '';

  try {
    const res = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    addMessage('bot', data.answer || data.error || "Sorry, I couldn't process that.");

  } catch (err) {
    addMessage('bot', "❌ Connection error. Please try again.");
  }
}

function suggestQuestion(q) {
  userInput.value = q;
  sendMessage();
}

// Press Enter to send
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});