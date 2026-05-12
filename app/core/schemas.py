from pydantic import BaseModel
from typing import List, Optional

class CustomerRequest(BaseModel):
    message_id: str
    customer_id: str
    message: str

class IntentOutput(BaseModel):
    intent: str
    confidence: float

class PriorityOutput(BaseModel):
    priority_level: str  # "low", "medium", "high"
    reason: str

class PolicyOutput(BaseModel):
    policy_text: str

class DraftOutput(BaseModel):
    draft_reply: str
    missing_info: Optional[List[str]] = []
    suggested_action: Optional[str] = None #

class ValidationOutput(BaseModel):
    is_valid: bool
    feedback: str

class RouterOutput(BaseModel):
    decision: str  # "send_reply", "ask_info", "escalate"

class WorkflowTrace(BaseModel):
    request: CustomerRequest
    intent_detection: Optional[IntentOutput] = None
    priority_assessment: Optional[PriorityOutput] = None
    policy_retrieval: Optional[PolicyOutput] = None
    response_drafting: Optional[DraftOutput] = None
    validation: Optional[ValidationOutput] = None
    final_routing: Optional[RouterOutput] = None

class AgentResponse(BaseModel):
    decision: str #
    final_reply: Optional[str] = None
    trace: WorkflowTrace #