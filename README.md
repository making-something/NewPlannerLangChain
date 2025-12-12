# AI Holiday Planner

An intelligent holiday planning application powered by Cerebras LLM with a FastAPI backend.

## Project Structure

```
NewPlanner/
├── backend/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── planner.py          # Holiday planner endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py      # Cerebras LLM service
│   ├── main.py                  # FastAPI application entry point
│   ├── models.py                # Pydantic request/response models
│   └── requirements.txt          # Backend dependencies
├── main.py                       # CLI version of the planner
├── openapi.yaml                  # OpenAPI specification
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Set Environment Variables

Create a `.env` file in the project root:

```
CEREBRAS_API_KEY=your_api_key_here
```

### 4. Run the Backend Server

```bash
cd backend
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI YAML**: http://localhost:8000/openapi.json

## API Endpoints

### Generate Itinerary
**POST** `/api/v1/planner/generate`

Create a new personalized itinerary based on user description.

**Request:**
```json
{
  "description": "I want a 7-day tropical vacation in Bali with a moderate budget..."
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "itinerary": "# 7-Day Bali Itinerary\n...",
  "follow_up_questions": [
    {
      "question": "Would you prefer beachfront or jungle accommodations?",
      "order": 1
    }
  ]
}
```

### Refine Itinerary
**POST** `/api/v1/planner/refine`

Refine an existing itinerary based on feedback.

**Request:**
```json
{
  "session_id": "uuid-string",
  "feedback": "I prefer more adventure activities..."
}
```

### Save Itinerary
**POST** `/api/v1/planner/save`

Save the current itinerary to a file.

**Request:**
```json
{
  "session_id": "uuid-string",
  "filename": "bali_trip"
}
```

### Get Session
**GET** `/api/v1/planner/sessions/{session_id}`

Retrieve the current state of a session.

### Delete Session
**DELETE** `/api/v1/planner/sessions/{session_id}`

Delete a session and its data.

## CLI Usage

To use the standalone CLI version:

```bash
python main.py
```

Follow the prompts to create and refine your holiday itinerary.

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Cerebras**: LLM provider for itinerary generation
- **Uvicorn**: ASGI server for running FastAPI
- **LangChain**: Framework for working with LLMs

## License

MIT
