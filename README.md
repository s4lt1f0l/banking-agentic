# Banking AI-Agent Microservices

FastAPI banking support agent with a Streamlit frontend, a gRPC intent service, and external Pinggy-tunneled model endpoints.

The app does not run Ollama or the intent model locally. You need active Pinggy URLs for both services.

## Services

- `api-gateway`: FastAPI backend on `http://localhost:8000`
- `intent-service`: gRPC service on `localhost:50051`
- `frontend`: Streamlit UI on `http://localhost:8502`
- External Ollama endpoint: `OLLAMA_BASE_URL`, exposing `/api/generate`
- External intent endpoint: `INTENT_API_URL`, exposing `/predict`

## Layer Architecture

```text
+--------------------------------------------------------------------------------+
|                                User Interface                                  |
|                                                                                |
|  Streamlit Frontend                                                            |
|  frontend/interface.py                                                         |
|  http://localhost:8502                                                         |
+----------------------------------------+---------------------------------------+
                                         |
                                         | HTTP POST /run-agent
                                         v
+--------------------------------------------------------------------------------+
|                                API Gateway                                     |
|                                                                                |
|  FastAPI Backend                                                               |
|  backend/app/main.py                                                           |
|  http://localhost:8000                                                         |
|                                                                                |
|  Endpoints:                                                                    |
|    GET  /health                                                                |
|    GET  /config                                                                |
|    POST /run-agent                                                             |
|    POST /support                                                               |
+----------------------------------------+---------------------------------------+
                                         |
                                         | BankingAgentOrchestrator
                                         v
+--------------------------------------------------------------------------------+
|                              Agent Workflow Layer                              |
|                                                                                |
|  backend/app/agent/orchestrator.py                                             |
|                                                                                |
|  1. IntentDetectionNode                                                        |
|  2. PriorityDetectionNode                                                      |
|  3. PolicyRetrievalNode                                                        |
|  4. ResponseDraftingNode                                                       |
|  5. ValidationNode                                                             |
|  6. RouterNode                                                                 |
+--------------------------+-----------------------------+-----------------------+
                           |                             |
                           | gRPC                        | HTTP /api/generate
                           v                             v
+----------------------------------------+     +---------------------------------+
|             Intent Service             |     |       External LLM Service      |
|                                        |     |                                 |
|  Python gRPC service                   |     |  Pinggy-tunneled Ollama API     |
|  intent_service/server.py              |     |  OLLAMA_BASE_URL                |
|  localhost:50051                       |     |  Model: LLM_MODEL               |
|                                        |     |                                 |
|  Validates labels against all          |     |  Drafts support reply from      |
|  77 Banking77 intents                  |     |  prompt + policy + trace data   |
+--------------------+-------------------+     +---------------------------------+
                     |
                     | HTTP POST /predict
                     v
+--------------------------------------------------------------------------------+
|                           External Intent Model API                            |
|                                                                                |
|  Pinggy-tunneled intent classifier                                             |
|  INTENT_API_URL                                                                |
|                                                                                |
|  Request:  {"message": "..."}                                                  |
|  Response: {"intent": "...", "confidence": 0.92, "reason": "..."}              |
+--------------------------------------------------------------------------------+
```

## Project Structure

```text
banking-agentic/
  backend/          FastAPI gateway and agent workflow nodes
  frontend/         Streamlit interface
  intent_service/   gRPC service and Banking77 intent client
  examples/         Sample request payloads
  tests/            Pytest tests
  docker-compose.yml
```

## Configuration

Create `.env` from `.env.example`:

```env
OLLAMA_BASE_URL=https://your-ollama-pinggy-url
LLM_MODEL=gpt-oss:20b
INTENT_API_URL=https://your-intent-pinggy-url/predict
```

Do not commit real Pinggy URLs or credentials.

## Run with Docker Compose

```bash
docker compose up --build
```

Open:

- Frontend: `http://localhost:8502`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## API

Run the agent workflow:

```bash
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-001",
    "customer_id": "cust-001",
    "message": "I have a suspicious card transaction that I do not recognize."
  }'
```

Endpoints:

- `GET /health`
- `GET /config`
- `POST /run-agent`
- `POST /support`

## Local Development

Run each service in a separate terminal:

```bash
cd intent_service
pip install -r requirements.txt
INTENT_API_URL=https://your-intent-pinggy-url/predict python server.py
```

```bash
cd backend
pip install -r requirements.txt
OLLAMA_BASE_URL=https://your-ollama-pinggy-url INTENT_SERVICE_HOST=localhost python run.py
```

```bash
cd frontend
pip install -r requirements.txt
streamlit run interface.py
```

## gRPC Stubs

Generated stubs are committed. Regenerate them after changing `intent_service/intent_service.proto`:

```bash
cd intent_service
make
```

If the proto changes, copy the regenerated stubs into `backend/app/clients/intent_grpc/`.

# Video demo

https://drive.google.com/file/d/130hNJXssGci3-A5b-f00ECyq_a6A0Dmu/view?usp=sharing
