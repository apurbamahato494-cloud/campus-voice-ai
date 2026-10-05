# 🎓 Campus Voice AI

An automated admission voice counselor built with FastAPI, SQLite, and Vapi to answer seat inquiries and register leads in real time.

## 🚀 Tech Stack
* **Voice Agent:** Vapi (Speech-to-Text & Text-to-Speech)
* **Backend:** FastAPI (Python)
* **Database:** SQLite3
* **Tunneling:** ngrok

## 🛠️ Setup
1. Install dependencies: `pip install fastapi uvicorn pydantic`
2. Run backend: `uvicorn main:app --reload`
3. Expose port: `ngrok http 8000`