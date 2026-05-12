# Banking AI-Agent

## Overall Objective
This project implements a simple AI agentic workflow for customer support in the banking domain. The system receives a customer message, identifies the corresponding intent using a fine-tuned model, retrieves relevant policy information, generates a draft response using a local LLM, and determines whether the case can be handled automatically or should be escalated to human staff.

## System Workflow
The banking agentic system follows a structured pipeline consisting of several specialized nodes orchestrated together:

1. **Intent Detection Node:** Identifies the customer's intent from the input message using a fine-tuned model (from Lab 2).
2. **Priority Detection Node:** Determines whether the issue is low, medium, or high priority based on the detected intent and keywords (e.g., suspicious transactions, blocked accounts).
3. **Policy Retrieval Node:** Retrieves relevant FAQ entries, policy snippets, or support guidelines based on the predicted intent to ground the final response.
4. **Response Drafting Node:** Calls an LLM (`gpt-oss-20b` via Ollama) to generate a draft reply taking into account the customer message, intent, priority, and retrieved policy.
5. **Validation Node:** Checks whether the generated response is acceptable (e.g., checks if the response is too short).
6. **Router Node:** Makes the final decision based on previous outputs to either:
   - Send the reply directly.
   - Ask the customer for more information.
   - Escalate the case to a human support team.

## Project Structure
- `app/main.py`: Entry point for the FastAPI application.
- `app/agent/orchestrator.py`: Implements the main workflow controller, calling nodes in the correct order and collecting intermediate outputs.
- `app/nodes/`: Contains the implementation for all workflow nodes (`intent_node.py`, `priority_node.py`, `policy_node.py`, `draft_node.py`, `validation_node.py`, `router_node.py`).
- `app/clients/`: Defines the base client interface and the specific Ollama client for model calling.
- `app/core/`: Contains application settings (`settings.py`) and Pydantic schemas for inputs, outputs, and trace formats (`schemas.py`).
- `app/data/`: Stores policy data and FAQ snippets (`policies.py`).
- `examples/sample_requests.json`: Example banking customer messages covering multiple intents for testing.

## Installation and Running Instructions

### Prerequisites
- Python 3.10+
- Access to external LLM endpoints (Ollama running `gpt-oss-20b` & Kaggle API for intent detection) configured via Pinggy tunnels.

### Installation
1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
Start the FastAPI development server using the provided script:
```bash
python run.py
```
The API will be available at `http://localhost:8000`. You can access the Swagger UI documentation at `http://localhost:8000/docs`.

### Testing
You can test the system using the provided sample requests:
```bash
python -c "import json, requests, sys; sys.stdout.reconfigure(encoding='utf-8'); results = [requests.post('http://localhost:8000/support', json=t).json() for t in json.load(open('examples/sample_requests.json', encoding='utf-8'))]; print(json.dumps(results, indent=2, ensure_ascii=False))"
```

## Video Demonstration
[Video demo](https://drive.google.com/file/d/1S3qwx2ADpm9FRq44rlpIWzURbra6MFIb/view?usp=sharing)
