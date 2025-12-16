# 🌐 Myapp – AI Holiday Planner Frontend

This is the Angular 18+ frontend for the AI Holiday Planner project. It provides a modern, responsive chat UI for generating, refining, and saving detailed travel itineraries using LLMs (Cerebras, OpenAI, Groq, and more).

---

## ✨ Features

- **Chatbot UI:** Clean, dark-themed chat interface with sidebar for chat history and quick templates.
- **Model Selection:** Instantly switch between LLM providers and models from the top bar.
- **Markdown Rendering:** Beautiful, clickable itineraries with Google Search links, headings, and tips.
- **Copy Tool:** Copy any AI response with a single click.
- **Session Management:** Start new chats, view and delete sessions.
- **Extensive Prompts:** Get highly detailed, actionable itineraries in a single response.

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Start the Development Server

```bash
npm start
```

Visit [http://localhost:4200](http://localhost:4200) in your browser.

---

## 🖥️ UI Overview

- **Sidebar:**
  - Chat history, quick templates, and "New Chat" button
- **Top Bar:**
  - Provider/model dropdowns (syncs with backend)
- **Chat Area:**
  - User and AI messages, markdown rendering, copy tool

![Chat UI Screenshot](../docs/chat-ui.png)

---

## 🛠️ Code Structure

```
myapp/
├── src/
│   └── app/
│       ├── components/
│       │   ├── chat/         # Chat UI logic
│       │   └── sidebar/      # Sidebar and chat list
│       ├── services/         # API communication
│       ├── models/           # TypeScript models
│       └── pipes/            # Markdown rendering
└── ...
```

---

## 🧑‍💻 Technologies Used

- **Angular 18+**
- **Tailwind CSS** (with typography plugin)
- **RxJS**
- **marked.js** (Markdown rendering)

---

## 📸 Visuals

> ![Sidebar and Chat Example](../docs/sidebar-example.png)
> *Sidebar with chat history, model selection, and new chat button.*
>
> ![Markdown Rendering Example](../docs/markdown-example.png)
> *Itinerary with headings, links, and copy tool.*

---

## 📚 Additional Resources

- [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli)
- [Project OpenAPI Spec](../openapi.yaml)

---

## 📝 License

MIT
