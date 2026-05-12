from fastapi import FastAPI
from app.core.schemas import CustomerRequest, AgentResponse
from app.agent.orchestrator import BankingAgentOrchestrator

app = FastAPI(title="Banking AI-Agent API") #
orchestrator = BankingAgentOrchestrator() #

@app.post("/support", response_model=AgentResponse) #
def handle_support(request: CustomerRequest):
    return orchestrator.process_request(request)