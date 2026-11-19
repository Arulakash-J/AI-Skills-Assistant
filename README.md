# AI Skills Assistant

A voice and chat assistant for the AI Skills Program. Users can type a question or speak into the mic. The assistant streams its answer back as text and reads it aloud. It can also raise support tickets and send emails, such as enrollment confirmations, callback requests and escalations.

## Features

- **Streaming chat:** answers appear word by word, using Google Gemini.
- **Live voice input:** speech is transcribed in real time with Deepgram (`nova-3`) over a WebSocket.
- **Spoken replies:** text-to-speech with ElevenLabs, which can be stopped at any time.
- **Tools the assistant can call:**
  - `raise_ticket`: saves a support ticket to `backend/data/tickets.json`.
  - `send_email`: sends an email through Gmail SMTP to the configured address.
- **Timing logs:** latency for chat, speech and tool calls is written to `backend/logs/timing.log`.

## Tech stack

| Part     | Technology                                          |
|----------|-----------------------------------------------------|
| Frontend | React 18, Vite 5                                    |
| Backend  | Python, FastAPI, Uvicorn                            |
| AI       | Google Gemini (chat), Deepgram (STT), ElevenLabs (TTS) |
| Email    | Gmail SMTP (app password)                           |

## Project structure

```
.
├── backend/
│   ├── app.py                  # FastAPI app and routes
│   ├── prompts/
│   │   └── system_prompt.py    # Assistant instructions and program knowledge
│   ├── services/
│   │   ├── chat_service.py     # Gemini streaming and tool handling
│   │   └── speech_service.py   # Deepgram STT and ElevenLabs TTS
│   ├── tools/
│   │   ├── email_tool.py       # send_email tool
│   │   └── ticket_tool.py      # raise_ticket tool
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.jsx             # Chat UI, voice recording, audio playback
    │   ├── main.jsx
    │   └── styles.css
    ├── public/                 # Static files (logo.png)
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── .env.example
```

## Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer
- API keys for Google Gemini, Deepgram and ElevenLabs
- A Gmail account with an [app password](https://support.google.com/accounts/answer/185833) if you want the email tool

## Getting started

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your keys
uvicorn app:app --reload --port 8000
```

To check that the server is running, open http://localhost:8000/health. It should return `{"status": "ok"}`.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local      # optional, defaults to http://localhost:8000
npm run dev
```

Open http://localhost:5173 and click **Start conversation**.

## Configuration

### Backend (`backend/.env`)

| Variable                | Required | Description                                              |
|-------------------------|----------|----------------------------------------------------------|
| `GEMINI_API_KEY`        | Yes      | Google Gemini API key                                    |
| `GEMINI_CHAT_MODEL`     | Yes      | Gemini model ID to use for chat                          |
| `GEMINI_THINKING_LEVEL` | No       | Thinking level for Gemini (default `low`)                |
| `DEEPGRAM_API_KEY`      | Yes      | Deepgram API key for live transcription                  |
| `ELEVENLABS_API_KEY`    | Yes      | ElevenLabs API key                                       |
| `ELEVENLABS_VOICE_ID`   | Yes      | ElevenLabs voice to speak with                           |
| `GMAIL_ADDRESS`         | Email    | Gmail account that sends the emails                      |
| `GMAIL_APP_PASSWORD`    | Email    | App password for that account                            |
| `EMAIL_TO`              | Email    | Address that receives emails from the assistant          |
| `FRONTEND_ORIGIN`       | No       | Allowed CORS origin (default `http://localhost:5173`)    |
| `LOG_FILE`              | No       | Path of the timing log (default `logs/timing.log`)       |

### Frontend (`frontend/.env.local`)

| Variable            | Description                                          |
|---------------------|------------------------------------------------------|
| `VITE_API_BASE_URL` | Backend URL (default `http://localhost:8000`)        |

## API

| Method    | Path               | Description                                                                 |
|-----------|--------------------|-----------------------------------------------------------------------------|
| GET       | `/health`          | Health check                                                                |
| POST      | `/chat/stream`     | Takes `{"messages": [{"role": "user", "content": "..."}]}` and streams the reply as server-sent events: `status`, `token`, `action`, `done`, `error` |
| WebSocket | `/speech/live`     | Send audio chunks, then `{"type": "stop"}`. Receives `partial`, `final` and `error` messages |
| GET       | `/speech/greeting` | Spoken greeting as MP3                                                      |
| GET       | `/speech/speak`    | `?text=...` returns the text spoken as MP3 (up to 3000 characters)          |

## Customizing the assistant

Edit [backend/prompts/system_prompt.py](backend/prompts/system_prompt.py) to change the assistant's instructions and the program information it answers from.

## Notes

- `backend/data/` (tickets) and `backend/logs/` are created at runtime and are not committed.
- Never commit `.env` files. Only the `.env.example` templates belong in the repo.
- Browsers only allow microphone access on `localhost` or over HTTPS.
