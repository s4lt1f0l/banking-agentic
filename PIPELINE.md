# Banking AI-Agent Pipeline

This project is a small microservice pipeline for handling banking support messages. The frontend collects a customer message, the API Gateway orchestrates agent nodes, the Intent Service classifies the message against Banking77 intents, and external Pinggy-tunneled model APIs provide intent prediction and response drafting.

## Layer Architecture

```text
+--------------------------------------------------------------------------------+
|                                User Interface                                  |
|                                                                                |
|  Streamlit Frontend                                                             |
|  frontend/interface.py                                                          |
|  http://localhost:8502                                                          |
+----------------------------------------+---------------------------------------+
                                         |
                                         | HTTP POST /run-agent
                                         v
+--------------------------------------------------------------------------------+
|                                API Gateway                                     |
|                                                                                |
|  FastAPI Backend                                                                |
|  backend/app/main.py                                                            |
|  http://localhost:8000                                                          |
|                                                                                |
|  Endpoints:                                                                     |
|    GET  /health                                                                 |
|    GET  /config                                                                 |
|    POST /run-agent                                                              |
|    POST /support                                                                |
+----------------------------------------+---------------------------------------+
                                         |
                                         | BankingAgentOrchestrator
                                         v
+--------------------------------------------------------------------------------+
|                              Agent Workflow Layer                              |
|                                                                                |
|  backend/app/agent/orchestrator.py                                              |
|                                                                                |
|  1. IntentDetectionNode                                                         |
|  2. PriorityDetectionNode                                                       |
|  3. PolicyRetrievalNode                                                         |
|  4. ResponseDraftingNode                                                        |
|  5. ValidationNode                                                              |
|  6. RouterNode                                                                  |
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
|  Pinggy-tunneled intent classifier                                              |
|  INTENT_API_URL                                                                 |
|                                                                                |
|  Request:  {"message": "..."}                                                   |
|  Response: {"intent": "...", "confidence": 0.92, "reason": "..."}              |
+--------------------------------------------------------------------------------+
```

## Runtime Flow

```text
Customer
  |
  | enters message
  v
Streamlit Frontend
  |
  | builds CustomerRequest:
  |   message_id, customer_id, message
  |
  | POST /run-agent
  v
FastAPI API Gateway
  |
  | calls BankingAgentOrchestrator.process_request()
  v
WorkflowTrace starts
  |
  +--> IntentDetectionNode
  |      |
  |      | gRPC IntentRecognizer(message)
  |      v
  |    Intent Service
  |      |
  |      | POST INTENT_API_URL
  |      v
  |    Pinggy Intent API
  |      |
  |      | returns intent, confidence, reason
  |      v
  |    validate against Banking77 labels
  |      |
  |      | returns IntentOutput
  |      v
  |
  +--> PriorityDetectionNode
  |      |
  |      | uses intent + message keywords
  |      v
  |    PriorityOutput: low, medium, or high
  |
  +--> PolicyRetrievalNode
  |      |
  |      | finds exact policy or category fallback
  |      v
  |    PolicyOutput
  |
  +--> ResponseDraftingNode
  |      |
  |      | sends prompt to OLLAMA_BASE_URL /api/generate
  |      v
  |    DraftOutput:
  |      draft_reply, missing_info, suggested_action
  |
  +--> ValidationNode
  |      |
  |      | checks whether draft is usable
  |      v
  |    ValidationOutput
  |
  +--> RouterNode
         |
         | combines priority, validation, and missing_info
         v
       RouterOutput:
         send_reply | ask_info | escalate
         |
         v
AgentResponse:
  decision, final_reply, trace
```

## Data Contracts

### CustomerRequest

```json
{
  "message_id": "msg-001",
  "customer_id": "cust-001",
  "message": "I have a suspicious card transaction that I do not recognize."
}
```

### AgentResponse

```json
{
  "decision": "send_reply",
  "final_reply": "Customer-facing reply or null when escalated.",
  "trace": {
    "request": {},
    "intent_detection": {},
    "priority_assessment": {},
    "policy_retrieval": {},
    "response_drafting": {},
    "validation": {},
    "final_routing": {}
  }
}
```

## Container Layout

```text
docker-compose.yml
  |
  +-- api-gateway
  |     build: backend/
  |     port: 8000
  |     depends_on: intent-service
  |     env: OLLAMA_BASE_URL, LLM_MODEL, INTENT_SERVICE_HOST, INTENT_SERVICE_PORT
  |
  +-- intent-service
  |     build: intent_service/
  |     port: 50051
  |     env: INTENT_API_URL
  |
  +-- frontend
        build: frontend/
        port: 8502
        depends_on: api-gateway
        env: API_BASE_URL=http://api-gateway:8000
```

## Main Files

```text
frontend/interface.py
  Streamlit UI and HTTP client to the API Gateway.

backend/app/main.py
  FastAPI app and public endpoints.

backend/app/agent/orchestrator.py
  Sequential agent workflow.

backend/app/nodes/
  Individual workflow nodes for intent, priority, policy, drafting, validation, and routing.

backend/app/data/policies.py
  Specific and category fallback policy guidance.

intent_service/server.py
  gRPC service entrypoint.

intent_service/classifier.py
  Calls the external intent API, normalizes legacy aliases, and validates allowed intents.

intent_service/banking77_intents.py
  Canonical list of all 77 Banking77 intent labels.
```

## Decision Logic

```text
high priority
  -> escalate

invalid draft
  -> escalate

missing required information
  -> ask_info

otherwise
  -> send_reply
```
