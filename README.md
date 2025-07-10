# CsPlayers API

A simple FastAPI application for managing CS players.

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**

   ```bash
   python main.py
   ```

   Or alternatively:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /players` - Get all players (placeholder data)

## Interactive API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

The application runs on `http://localhost:8000` with auto-reload enabled for development.
