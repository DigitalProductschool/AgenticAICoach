let ws;
const chatBox = document.getElementById("chat");

function addBubble(sender, text, type) {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.classList.add(type === "agent" ? "agent-bubble" : "user-bubble");

  bubble.innerHTML = `
    <div class="sender">${sender}</div>
    <div>${text}</div>
  `;

  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function start() {
  const pitch = document.getElementById("pitchInput").value;
  if (!pitch.trim()) return alert("Enter your startup pitch first!");

  // ws = new WebSocket("ws://127.0.0.1:8000/ws");
  ws = new WebSocket("wss://ai-pitch-coach-6uw3.onrender.com/ws");

  ws.onopen = () => {
    addBubble("Founder", pitch, "user");
    ws.send(JSON.stringify({ pitch }));
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      addBubble(data.agent, data.message, "agent");
    } catch {
      addBubble("System", event.data, "agent");
    }
  };
}

const replyInput = document.getElementById("replyInput");
const micBtn = document.getElementById("micBtn");
const improveBtn = document.getElementById("improveBtn");
const sendBtn = document.getElementById("sendBtn");
const textStatus = document.getElementById("status");

/* Helper: show status */
function showStatus(text, loading=false) {
  textStatus.innerText = text;
  textStatus.classList.add("active");

  if (loading) textStatus.classList.add("loading");
  else textStatus.classList.remove("loading");
}

/* Helper: clear status */
function clearStatus() {
  textStatus.classList.remove("active");
  textStatus.classList.remove("loading");
}

// 🎤 Mic Recording
let mediaRecorder;
let audioChunks = [];
let stream;

micBtn.onclick = async () => {
  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    await startRecording();
  } else {
    stopRecording();
  }
};

async function startRecording() {
  stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.start();
  micBtn.innerText = "🛑";
  showStatus("Recording...");

  // Disable typing + sending
  replyInput.disabled = true;
  replyInput.classList.add("recording");
  sendBtn.disabled = true;

  audioChunks = [];
  mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
}

function stopRecording() {
  mediaRecorder.stop();
  micBtn.innerHTML = `
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="2" width="6" height="12" rx="3"></rect>
            <path d="M5 10v2a7 7 0 0 0 14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="22"></line>
          </svg>`;
  showStatus("Transcribing audio...", true);

  // Turn off mic hardware
  if (stream) stream.getTracks().forEach(track => track.stop());

  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", blob);

    let res = await fetch("/get-transcription", {
      method: "POST",
      body: formData
    });
    
    setTimeout(clearStatus, 200);

    const data = await res.json();
    replyInput.value = data.transcript;
  
    // Re-enable input + send
    replyInput.disabled = false;
    replyInput.classList.remove("recording");
    sendBtn.disabled = false;
  };
}

// Refine user's reply 
improveBtn.onclick = async () => {
  const text = replyInput.value;
  if (!text.trim()) return;

  replyInput.value = ""
  showStatus("Refining your reply...", true);

  const res = await fetch("/improve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const data = await res.json();

  setTimeout(clearStatus, 200);
  replyInput.value = data.improved;
};

// Send user's reply 
sendBtn.onclick = async () => {
  const reply = replyInput.value;

  if (!reply.trim()) return;

  addBubble("Founder", reply, "user");
  ws.send(JSON.stringify({ reply }));

  replyInput.value = "";
}
