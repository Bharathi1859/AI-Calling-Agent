# AI Calling Agent MVP

An AI-powered two-way voice calling agent built using **Python, FastAPI, Gemini GenAI, Faster-Whisper, Edge TTS, PostgreSQL, and Next.js**.

The application demonstrates an automated calling workflow where an administrator can create customers, initiate a call simulation, communicate with the AI agent through voice, maintain conversation context, extract customer requirements, generate AI responses, and persist call/conversation data in PostgreSQL.

> **Demo Mode:**
> This project uses a browser-based voice calling simulation for development and demonstration. It does not require a paid telephony subscription. The calling layer is designed so that a real telephony provider can be integrated in the future.

---

## 1. Project Objective

The objective of this project is to demonstrate the core architecture of an AI-powered calling agent capable of:

* Managing customer information
* Initiating an outbound call session
* Capturing customer speech
* Converting speech to text
* Understanding customer responses using GenAI
* Maintaining conversation context
* Identifying missing customer information
* Asking relevant follow-up questions
* Converting AI responses to speech
* Storing call and conversation information in PostgreSQL
* Providing an administrative dashboard

The system is designed as an MVP that can later be extended with a production telephony provider and real-time communication infrastructure.

---

# 2. Key Features

### Customer Management

Administrators can:

* Add customers
* Store customer phone numbers
* Store company information
* Store enquiry purpose
* Store product information
* View customer records

Example:

```text
Customer Name: Rahul Kumar
Phone Number: +91XXXXXXXXXX
Company: ABC Hotels
Purpose: Product enquiry
Product: Commercial RO System
```

### Call Management

The dashboard supports:

* Starting a call session
* Tracking call status
* Ending/completing a call
* Recording call start/end time
* Calculating call duration
* Maintaining call history

### AI Voice Conversation

The browser-based voice workflow is:

```text
Customer Speech
      ↓
Speech-to-Text
      ↓
Gemini AI Agent
      ↓
Conversation State
      ↓
AI Response
      ↓
Text-to-Speech
      ↓
Customer Audio
```

The conversation can continue over multiple turns.

### Agentic Conversation Context

The AI agent maintains structured conversation state instead of treating every message as an independent request.

The agent tracks information such as:

```text
Customer Name
Company Name
Requirement
RO Capacity
Location
Application
Budget
Timeline
```

The agent identifies which fields are already known and generates the next question based on missing information.

For example:

```text
AI:
What RO capacity are you looking for?

Customer:
Around 500 LPH.

AI:
Great. Which city will the system be installed in?
```

The agent can retain previously collected information instead of repeatedly asking for it.

---

# 3. Technology Stack

| Component         | Technology                               |
| ----------------- | ---------------------------------------- |
| Backend           | Python                                   |
| API Framework     | FastAPI                                  |
| LLM / GenAI       | Google Gemini                            |
| Agent Logic       | Python-based conversation state + Gemini |
| Speech-to-Text    | Faster-Whisper                           |
| Text-to-Speech    | Edge TTS                                 |
| Database          | PostgreSQL                               |
| ORM               | SQLAlchemy                               |
| Frontend          | Next.js                                  |
| Frontend Language | TypeScript                               |
| UI                | Tailwind CSS                             |
| Voice Input       | Browser MediaRecorder API                |
| API Testing       | FastAPI Swagger/OpenAPI                  |

---

# 4. System Architecture

```text
                    ┌──────────────────────┐
                    │   Next.js Dashboard  │
                    │      Admin UI        │
                    └──────────┬───────────┘
                               │
                               │ REST API
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI Backend  │
                    │                      │
                    │ Customer APIs        │
                    │ Call APIs            │
                    │ Conversation APIs    │
                    │ Voice API            │
                    └───────┬───────┬──────┘
                            │       │
                 ┌──────────┘       └──────────┐
                 ▼                             ▼
        ┌────────────────┐            ┌─────────────────┐
        │  PostgreSQL    │            │   AI Pipeline   │
        │                │            │                 │
        │ Customers      │            │ Faster-Whisper  │
        │ Calls          │            │      ↓          │
        │ Conversations  │            │ Gemini Agent    │
        │ Call Summary   │            │      ↓          │
        └────────────────┘            │    Edge TTS     │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      Browser Audio Output
```

---

# 5. Project Structure

```text
AI_calling_agent/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── calls.py
│   │   │   ├── customers.py
│   │   │   ├── conversations.py
│   │   │   └── voice.py
│   │   │
│   │   ├── agent/
│   │   │   ├── agent.py
│   │   │   ├── state.py
│   │   │   └── state_service.py
│   │   │
│   │   ├── models/
│   │   │   ├── customer.py
│   │   │   ├── call.py
│   │   │   ├── conversation.py
│   │   │   └── summary.py
│   │   │
│   │   ├── voice/
│   │   │   ├── stt.py
│   │   │   └── tts.py
│   │   │
│   │   ├── database.py
│   │   ├── schemas.py
│   │   ├── call_schemas.py
│   │   ├── conversation_schemas.py
│   │   └── main.py
│   │
│   ├── create_tables.py
│   └── test_audio/
│
├── frontend/
│   ├── dashboard/
│   │   └── app/
│   │       └── page.tsx
│   │
│   └── voice-test/
│       └── index.html
│
├── database/
├── docs/
├── .gitignore
├── .env.example
└── README.md
```

---

# 6. AI Agent Workflow

The AI agent follows a structured state-based approach.

### Step 1 — Load Customer Information

When a call begins, existing customer information is loaded.

```text
Customer Name
Company
Product
Purpose
```

### Step 2 — Receive Customer Message

The customer's voice is converted to text using Faster-Whisper.

Example:

```text
"I need a commercial RO system for my hotel."
```

### Step 3 — Process Using Gemini

The message is passed to the Gemini-powered agent.

The agent evaluates the conversation and updates the structured state.

Example:

```text
Requirement = Commercial RO System
Application = Hotel
```

### Step 4 — Identify Missing Information

The agent checks which required information is still missing.

For example:

```text
Capacity
Location
Budget
Timeline
```

### Step 5 — Generate Next Question

The agent generates a relevant follow-up question based on the missing information.

### Step 6 — Save State

The updated conversation state is persisted in PostgreSQL.

### Step 7 — Generate Voice Response

The generated AI response is converted to speech using Edge TTS.

---

# 7. Voice Processing Workflow

The browser provides microphone input using the MediaRecorder API.

```text
Browser Microphone
       ↓
Audio Recording
       ↓
FastAPI /voice/process/{call_id}
       ↓
Faster-Whisper
       ↓
Customer Text
       ↓
Gemini Agent
       ↓
AI Text Response
       ↓
Edge TTS
       ↓
MP3 Audio
       ↓
Browser Playback
```

This provides a browser-based demonstration of the two-way voice interaction required by the assignment.

---

# 8. Database Design

PostgreSQL is used for persistent application data.

## Customers

Stores customer/contact information.

```text
customers
├── id
├── name
├── phone
├── company_name
├── purpose
├── product
└── created_at
```

## Calls

Stores call information.

```text
calls
├── id
├── customer_id
├── provider_call_id
├── direction
├── status
├── start_time
├── end_time
├── duration
├── outcome
├── lead_status
├── follow_up_required
├── error_message
└── created_at
```

## Conversation Messages

Stores each conversation turn.

```text
conversation_messages
├── id
├── call_id
├── speaker
├── message
└── timestamp
```

Example:

```text
Customer:
I need a 500 LPH RO system.

AI:
Sure. May I know your location?

Customer:
Bangalore.
```

## Call Summaries

Stores structured conversation information and summary-related fields.

```text
call_summaries
├── id
├── call_id
├── requirement
├── capacity
├── location
├── application
├── budget
├── timeline
├── customer_intent
├── key_points
├── follow_up_required
├── summary
└── created_at
```

---

# 9. API Endpoints

FastAPI automatically provides interactive API documentation.

After starting the backend, open:

```text
http://127.0.0.1:8000/docs
```

### Customer APIs

```text
POST   /customers
GET    /customers
GET    /customers/{customer_id}
PUT    /customers/{customer_id}
DELETE /customers/{customer_id}
```

### Call APIs

```text
POST   /calls
GET    /calls
GET    /calls/{call_id}
PATCH  /calls/{call_id}/status
```

### Conversation APIs

```text
POST /conversations
GET  /conversations/call/{call_id}
POST /conversations/call/{call_id}/message
```

### Voice API

```text
POST /voice/process/{call_id}
```

### Health Check

```text
GET /health
```

---

# 10. Environment Variables

Create a `.env` file inside the backend project.

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ai_calling_agent
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Do not commit the real `.env` file to GitHub.

Only `.env.example` should be committed.

---

# 11. PostgreSQL Setup

Create a PostgreSQL database named:

```text
ai_calling_agent
```

Example:

```sql
CREATE DATABASE ai_calling_agent;
```

Then configure the database connection in `.env`.

Create the application tables:

```powershell
python create_tables.py
```

Expected output:

```text
Creating database tables...
Database tables created successfully!
```

---

# 12. Backend Setup

Open PowerShell and navigate to the backend directory:

```powershell
cd backend
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required dependencies.

Then start FastAPI:

```powershell
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

# 13. Frontend Setup

Navigate to the dashboard:

```powershell
cd frontend\dashboard
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Open:

```text
http://localhost:3000
```

---

# 14. Browser Voice Demo

A separate browser-based voice testing page is included.

Navigate to:

```powershell
cd frontend\voice-test
```

Start the local server:

```powershell
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

Allow microphone permission when prompted.

The browser voice demo can:

1. Record customer speech
2. Send audio to FastAPI
3. Convert speech to text
4. Process the message through the Gemini agent
5. Generate an AI response
6. Convert the response to speech
7. Play the generated response

---

# 15. How to Test the Application

### Step 1

Start PostgreSQL.

### Step 2

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

### Step 3

Start Next.js:

```powershell
npm run dev
```

### Step 4

Open:

```text
http://localhost:3000
```

### Step 5

Add a customer.

Example:

```text
Name: Rahul Kumar
Phone: +919876543210
Company: ABC Hotels
Purpose: Product enquiry
Product: Commercial RO System
```

### Step 6

Click:

```text
Start Call
```

### Step 7

Use the browser microphone to speak.

### Step 8

The application processes the voice through:

```text
STT → Gemini Agent → TTS
```

### Step 9

Continue the conversation using multiple turns.

### Step 10

Click:

```text
End Call
```

The call status is updated and the call information remains stored in PostgreSQL.

---

# 16. Calling Implementation

The assignment allows a browser/WebRTC or simulated calling implementation when a free/trial telephony provider cannot be used for unrestricted outbound calling.

This project therefore uses a **browser-based voice simulation** for development and demonstration.

The architecture keeps call management separate from the AI conversation layer so that a real telephony provider can be integrated later.

A production implementation could replace the browser simulation with a provider such as Twilio or another compatible voice API.

---

# 17. AI and Voice Technologies

### GenAI

**Google Gemini**

Used for:

* Understanding customer responses
* Extracting structured information
* Maintaining conversation context
* Generating relevant follow-up questions
* Generating AI responses

### Speech-to-Text

**Faster-Whisper**

Used to convert customer speech into text locally.

Advantages:

* Open-source
* Local processing
* No per-minute speech API requirement for the demo

### Text-to-Speech

**Edge TTS**

Used to generate spoken AI responses.

The demo uses:

```text
en-US-AriaNeural
```

---

# 18. Error Handling

The application includes basic handling for:

* Customer not found
* Call not found
* Invalid API requests
* Empty speech input
* Speech recognition failure
* AI processing errors
* Microphone permission errors
* Failed voice processing requests
* Call status errors

Call records also contain an `error_message` field for recording call-related errors.

---

# 19. Security

Sensitive credentials are stored using environment variables.

The following should never be committed:

```text
.env
API keys
Database passwords
Secret credentials
```

The repository should contain:

```text
.env.example
```

instead of the actual `.env` file.

---

# 20. Current MVP Scope

The current implementation focuses on demonstrating the core AI calling workflow:

```text
Customer
   ↓
Browser Voice
   ↓
Speech-to-Text
   ↓
GenAI Agent
   ↓
Conversation Context
   ↓
Text-to-Speech
   ↓
Browser Audio
   ↓
PostgreSQL
```

The core components are implemented as separate modules so they can be extended independently.

---

# 21. Current Demo Limitations

This project is a development/MVP implementation.

### Telephony

A real outbound PSTN phone call is not included in the current demo.

Instead, browser-based voice simulation is used to demonstrate the same AI conversation pipeline without requiring a paid telephony subscription.

### Real-Time Streaming

The current browser implementation uses recorded audio chunks rather than a production-grade streaming audio/WebSocket pipeline.

### Dashboard Analytics

The current dashboard provides basic call statistics such as:

* Total customers
* Total calls
* Completed calls
* Active calls

Additional analytics can be added in a production version.

### Advanced Call Search

Advanced filtering by date, lead status, outcome, and follow-up status is planned as a future enhancement.

### Post-Call Summarization

The application stores structured conversation state and summary-related fields. A dedicated post-call LLM summarization workflow can be added to generate a final consolidated call summary automatically after every completed call.

---

# 22. Future Improvements

Possible production improvements include:

* Twilio or another telephony provider integration
* WebSocket-based real-time audio streaming
* Real-time speech interruption handling
* Voice activity detection
* Improved speech recognition
* Production-grade TTS streaming
* Automatic post-call AI summarization
* Advanced lead scoring
* Call search and filtering
* Detailed call-history pages
* Follow-up scheduling
* Authentication and role-based access
* Background task processing
* Retry mechanisms for external APIs
* Monitoring and logging
* Docker deployment
* Cloud deployment
* Automated testing
* Production database migrations

---

# 23. Conclusion

This project demonstrates an end-to-end architecture for an AI-powered calling agent using Python, FastAPI, GenAI, Speech-to-Text, Text-to-Speech, PostgreSQL, and Next.js.

The MVP demonstrates the essential AI calling workflow:

```text
Admin
  ↓
Customer Management
  ↓
Call Initiation
  ↓
Browser Voice Interaction
  ↓
Speech-to-Text
  ↓
Gemini Agent
  ↓
Context & Requirement Extraction
  ↓
AI Response
  ↓
Text-to-Speech
  ↓
Conversation Persistence
  ↓
PostgreSQL
```

The system is structured to allow future integration with a production telephony provider and real-time communication infrastructure.

---

## 24. Author

**Bharathi Jagadeesan**

B.E. Computer Science and Engineering

AI Calling Agent MVP — Technical Assignment
