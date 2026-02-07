# AI Voice Orchestration System

A real-time AI voice orchestration system with agentic architecture, separating orchestration logic from conversational intelligence using Django, FastAPI, and advanced AI models.

## 🎯 Features

- **Multi-Agent System**: 7 specialized agent categories (Medical, Nutrition, Finance, Legal, Research, Interview, General)
- **Real-time Chat**: WebSocket-based bidirectional communication
- **Intent Classification**: Qwen 2.5 model for intelligent message routing
- **Context-Aware Conversations**: Llama 3.1 with session memory
- **Speech-to-Text**: Whisper integration for voice input
- **REST API**: Django-based agent management with JWT authentication

---

## 📌 What Runs Where (Important)

| Service    | Port  | Purpose                    |
| ---------- | ----- | -------------------------- |
| Django API | 8000  | Agent creation, login, JWT |
| FastAPI    | 8001  | Real-time WebSocket chat   |
| Ollama     | 11434 | Local AI models (Qwen)     |
| React      | 3000  | Frontend UI                |

⚠️ **All services must be running together**

---

## 🧰 Prerequisites

Make sure these are installed:

* Python **3.10+**
* Node.js **18+**
* Ollama → [https://ollama.com](https://ollama.com)
* Groq API Key

---

## 🚀 Backend Setup (Python)

### 1️⃣ Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### 2️⃣ Add Environment Variables

Create a file:
`backend/.env`

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

### 3️⃣ Setup Django Database

```bash
cd backend/core
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

👤 Use this admin account to log in from the frontend.

---

## ▶️ Start All Services (VERY IMPORTANT)

You need **4 terminals open**.

---

### 🟢 Terminal 1 — Django Server (Port 8000)

```bash
cd backend/core
python manage.py runserver
```

Open:
👉 [http://localhost:8000](http://localhost:8000)

---

### 🟢 Terminal 2 — FastAPI WebSocket (Port 8001)

```bash
cd backend
python -m streaming.main
```

Open:
👉 [http://localhost:8001](http://localhost:8001)

---

### 🟢 Terminal 3 — Ollama (Local AI Models)

```bash
ollama pull qwen2.5:7b
ollama serve
```

Runs on:
👉 [http://localhost:11434](http://localhost:11434)

---

### 🟢 Terminal 4 — Frontend (Port 3000)

```bash
cd frontend
npm install
npm run dev
```

Open:
👉 [http://localhost:3000](http://localhost:3000)

---

## 🧪 (Optional) Test AI Logic

```bash
cd backend
python ai/test_ai.py
```

---

## 🧑‍💻 How to Use the App

### 1️⃣ Create an Agent

* Open [http://localhost:3000](http://localhost:3000)
* Click **Create Agent**
* Login using Django superuser
* Fill the form and submit

---

### 2️⃣ Start Chat

* Go to **Agents Page**
* Click **Start Chat**
* Send messages in real time

---

## 🛠️ Common Issues & Fixes

### ❌ WebSocket not connecting

* Make sure FastAPI is running on **8001**
* Check this file:

```js
frontend/src/services/websocket.js
```

```js
const WS_BASE_URL = "ws://localhost:8001";
```

---

### ❌ Qwen model not found

```bash
ollama pull qwen2.5:7b
```

---

### ❌ AI not responding

* Check `.env` file
* Verify `GROQ_API_KEY`
* Ensure Ollama is running

---

## 📁 Project Structure

```
ai-voice-orchestration-system/
├── backend/
│   ├── ai/          # AI logic
│   ├── core/        # Django project
│   └── streaming/   # FastAPI WebSocket
├── frontend/        # React app
└── docs/            # Postman collection
```

---

## 👤 Author

**Suman Kumari**
GitHub: [https://github.com/sSumankumari](https://github.com/sSumankumari)
