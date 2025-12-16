# 🌴 AI Holiday Planner

An intelligent, full-stack holiday planning application powered by FastAPI, Angular, and LLMs (Cerebras, OpenAI, Groq, and more). Effortlessly generate, refine, and save detailed travel itineraries with a beautiful, modern UI.

---

## 🗂️ Project Structure

```
NewPlanner/
├── backend/                # FastAPI backend (API, LLM integration, session management)
│   ├── routes/
│   │   └── planner.py      # Main API endpoints
│   ├── services/
│   │   └── llm_service.py  # LLM provider logic (Cerebras, OpenAI, Groq)
│   ├── main.py             # FastAPI app entry point
│   ├── models.py           # Pydantic models
│   └── requirements.txt    # Backend dependencies
├── myapp/                  # Angular 18+ frontend (chat UI, markdown rendering)
│   ├── src/
│   │   └── app/
│   │       ├── components/ # Chat, sidebar, etc.
│   │       ├── services/   # API communication
│   │       └── models/     # TypeScript models
│   └── ...
├── openapi.yaml            # OpenAPI 3.0 spec (API docs)
├── .env                    # Environment variables
└── README.md               # This file
```

---

## 🚀 Quickstart

### 1. Backend Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
cd backend
pip install -r requirements.txt
```

### 2. Frontend Setup
```bash
cd myapp
npm install
```

### 3. Environment Variables
Create a `.env` in the project root:
```
CEREBRAS_API_KEY=your_cerebras_key
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
DEFAULT_PROVIDER=cerebras
DEFAULT_MODEL=llama-3.3-70b
```

### 4. Run the App
- **Backend:**
  ```bash
  cd backend
  uvicorn main:app --reload
  ```
- **Frontend:**
  ```bash
  cd myapp
  npm start
  ```

---

## 🖥️ Features & UI

- **Chatbot UI:** Modern, responsive chat interface with sidebar for chat history and quick templates.
- **Model Selection:** Switch between LLM providers (Cerebras, OpenAI, Groq) and models from the frontend.
- **Markdown Rendering:** Beautiful, clickable itineraries with Google Search links, headings, and tips.
- **Copy Tool:** Instantly copy any AI response with a single click.
- **Session Management:** Start new chats, view and delete sessions.
- **Extensive Prompts:** Get highly detailed, actionable itineraries in a single response.

![Chat UI Screenshot](docs/chat-ui.png)

---

## 🛠️ API Endpoints (OpenAPI)

See [`openapi.yaml`](openapi.yaml) for full details. Key endpoints:

| Endpoint                                 | Method | Description                                 |
|------------------------------------------|--------|---------------------------------------------|
| `/api/v1/planner/models`                 | GET    | List available LLM providers/models          |
| `/api/v1/planner/generate`               | POST   | Generate a new itinerary                    |
| `/api/v1/planner/refine`                 | POST   | Refine an existing itinerary                |
| `/api/v1/planner/save`                   | POST   | Save itinerary to file                      |
| `/api/v1/planner/sessions/{session_id}`  | GET    | Get session state                           |
| `/api/v1/planner/sessions/{session_id}`  | DELETE | Delete a session                            |
| `/api/v1/planner/config/model`           | POST   | Update default provider/model in backend     |

---

## 🧑‍💻 Technologies Used

- **Backend:** FastAPI, Pydantic, LangChain, Uvicorn
- **Frontend:** Angular 18+, Tailwind CSS, RxJS, marked.js
- **LLMs:** Cerebras, OpenAI, Groq (pluggable)
- **Other:** Markdown rendering, Google Search links, session management

---

## 📄 License

MIT

---

## ✨ Screenshots

> ![Sidebar and Chat Example](docs/sidebar-example.png)
> *Sidebar with chat history, model selection, and new chat button.*

> ![Markdown Rendering Example](docs/markdown-example.png)
> *Itinerary with headings, links, and copy tool.*

---

## 🤝 Contributing

Pull requests and issues are welcome! Please see the [OpenAPI spec](openapi.yaml) and code comments for guidance.
