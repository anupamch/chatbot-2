# Local LLM API

Running a local LLM to respond to user prompts completely offline. It is a chatbot. Used gpt-2

## Features

- Local-first architecture
- FastAPI-based REST API
- Hugging Face Transformers integration
- Request/response logging to disk
- Offline operation

## Endpoints

### POST /generate

Generate a response from the local LLM.

**Request:**
```json
{
    "prompt": "Hello, who are you?"
}
```

**Response:**
```json
{
    "response": "I'm a local AI model, running offline!"
}
```

## Getting Started

1. Ensure you have Python 3.7+ installed
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, visit:
- OpenAPI documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`
- In Swagger all api are available and request format also response 
## Logs

Interactions are logged to the `logs` directory in JSON format, with one file per day.

## CLI

A CLI has added. Run the server first: python app.py. 
Open another terminal and run this:  python cli.py "What is artificial intelligence?"
