# 🎯 AI Pitch Coach Web Application (CrewAI + FastAPI)

AI Pitch Coach is a web-based assistant designed to help AI founders and entrepreneurs craft, refine, and deliver compelling startup pitches for investors, customers, or partners.

The application provides structured coaching, real-time feedback, voice transcription, and professional pitch rewriting through CrewAI agents.

---

## 🚀 Key Features

✅ Step-by-step startup pitch coaching conversation  
✅ Real-time AI chat using WebSockets  
✅ Voice message recording inside the chat input  
✅ Automatic speech-to-text transcription  
✅ Refine text button to rewrite unstructured text professionally  
✅ Clean WhatsApp-style chat UI  

---

## 🧠 What This App Does

AI Pitch Coach helps users with:

### 1. Structuring a Strong Startup Pitch
- Define the core problem  
- Explain the AI solution clearly  
- Highlight the unique value proposition (UVP)  

### 2. Refining Pitch Messaging & Delivery
- Improve clarity and logical flow  
- Remove filler words and repetition  
- Simplify complex AI concepts for investors  

### 3. Practicing Investor Q&A Scenarios
- Simulate realistic investor questions  
- Prepare confident responses to objections  

### 4. Iterative Pitch Improvement
- Users can resubmit updated pitches  
- The coach provides refined suggestions each round  

---

# 🛠 How the Application Works

## Step 1 — Start Coaching

When the user opens the application, they see a field at the top:

> "Describe your startup to begin coaching."

The founder enters a short startup description and clicks:

🚀 **Start Coaching**

This sends the message to the backend, where CrewAI starts the coaching workflow.

---

## Step 2 — Real-Time Pitch Coach Chat

After starting:

- The AI Pitch Coach begins an interactive structured chat  
- The founder replies step by step  
- The coach provides warm, supportive, actionable feedback  

---

## Step 3 — Voice Recording + Transcription

At the bottom of the page, the founder has a modern chat composer.

They can:

🎙️ Click the microphone button  
Speak naturally (messy and unstructured is okay)

The system will:

- Record audio  
- Send it to the backend  
- Return the transcription inside the textarea automatically  

---

## Step 4 — Refine text Button (Professional Rewrite)

Transcribed text may be:

- unclear  
- repetitive  
- too long  
- unstructured  
- full of filler words  

The founder can click:

🗯 **Refine**

The CrewAI improvement agent rewrites the message into a clear, professional investor-ready pitch while keeping the exact meaning.

Example:

Raw transcription:

> "So yeah we build like AI platform for warehouses and safety stuff..."

Refined output:

> "We are building an AI-powered safety monitoring platform for warehouses to detect risks early and reduce workplace accidents."

---

## Step 5 — Sending the Message

Once ready, the founder clicks:

➤ **Send**

After sending:
 
- The AI coach responds in real time  

---

# ⚙️ Installation & Running the Project (Step-by-Step)

Follow these steps to run the application locally and reproduce results.

---

## 1. Open the Project Directory

Navigate into the project folder:

```bash
cd path/to/your/project
```

---

## 2. Install Dependencies with Poetry

Lock and install all required packages:

```bash
poetry lock
poetry install --no-root
```

---

## 3. Activate the Poetry Virtual Environment

Enter the Poetry shell:

```bash
poetry shell
```

---

# 🔑 OpenAI API Key Setup (Required)

This project uses OpenAI models through CrewAI, so you must provide your own OpenAI API key.

---

## 4. Create a `.env` File

Inside the root directory of the project, create a file named:

```bash
.env
```

---

## 5. Add Your OpenAI API Key

Open the `.env` file and paste:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Example:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 6. Start the FastAPI Backend Server

Run the application:

```bash
uvicorn main:app --reload
```

You should see output like:

```
Uvicorn running on http://127.0.0.1:8000
```

---

## 7. Open the Web Application

Open your browser and go to:

```
http://127.0.0.1:8000
```

The AI Pitch Coach interface will load immediately.




