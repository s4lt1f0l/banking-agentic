from app.clients.ollama_client import OllamaClient
from app.core.schemas import DraftOutput, CustomerRequest, IntentOutput, PriorityOutput, PolicyOutput

class ResponseDraftingNode:
    def __init__(self):
        self.client = OllamaClient()

    def execute(self, request: CustomerRequest, intent_out: IntentOutput, 
                priority_out: PriorityOutput, policy_out: PolicyOutput) -> DraftOutput:
        
        prompt = f"""You are a professional banking support agent. Draft a polite reply strictly following the policy below.
        
Customer Message: "{request.message}"
Detected Intent: {intent_out.intent}
Priority Level: {priority_out.priority_level}
Policy Guideline: "{policy_out.policy_text}"

Draft a clear response in the language of the customer. Ask for necessary trace IDs or account details politely if the policy mentions it.
"""
        draft_text = self.client.generate(prompt)
        
        missing = []
        suggested = "send_reply"
        
        # Đưa ra đề xuất hành động tiếp theo nếu thấy thiếu thông tin quan trọng
        policy_lower = policy_out.policy_text.lower()
        msg_lower = request.message.lower()
        
        if "trace id" in policy_lower and "trace id" not in msg_lower:
            missing.append("Trace ID")
        if "số tài khoản" in policy_lower and not any(char.isdigit() for char in msg_lower):
            missing.append("Số tài khoản")
            
        if missing:
            suggested = "ask_info"

        return DraftOutput(draft_reply=draft_text, missing_info=missing, suggested_action=suggested)