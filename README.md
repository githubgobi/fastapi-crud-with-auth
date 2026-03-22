# FastAPI CRUD with Auth

A FastAPI application with CRUD operations and authentication, containerized with Docker.

## Setup

1. Ensure Docker is installed on your system.

2. Clone or navigate to this directory.

## Running the Application

### Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

This will build the Docker image and start the application on `http://localhost:8000`.

### Using Docker directly

```bash
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /items/{item_id}` - Get an item by ID

## Development

To run locally without Docker:

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `uvicorn main:app --reload`

## Troubleshooting

- Ensure port 8000 is not in use.
- If you encounter permission issues, try running Docker commands with `sudo` (on Linux/Mac).