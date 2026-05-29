from fastapi import FastAPI
from app.core.schemas import CustomerRequest, AgentResponse
from app.core.settings import settings
from app.agent.orchestrator import BankingAgentOrchestrator

app = FastAPI(title="Banking AI-Agent API Gateway") #
orchestrator = BankingAgentOrchestrator() #

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}

@app.get("/config")
def config():
    return {
        "ollama_base_url_configured": bool(settings.OLLAMA_BASE_URL),
        "llm_model": settings.LLM_MODEL,
        "intent_service_host": settings.INTENT_SERVICE_HOST,
        "intent_service_port": settings.INTENT_SERVICE_PORT,
    }

@app.post("/run-agent", response_model=AgentResponse)
def run_agent(request: CustomerRequest):
    return orchestrator.process_request(request)

@app.post("/support", response_model=AgentResponse) #
def handle_support(request: CustomerRequest):
    return run_agent(request)
