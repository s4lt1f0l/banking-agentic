from app.core.schemas import RouterOutput, PriorityOutput, ValidationOutput, DraftOutput

class RouterNode:
    def execute(self, priority_out: PriorityOutput, validation_out: ValidationOutput, draft_out: DraftOutput) -> RouterOutput: 
        if priority_out.priority_level == "high" or not validation_out.is_valid:
            return RouterOutput(decision="escalate") 
        
        if draft_out.missing_info:
            return RouterOutput(decision="ask_info") 
        
        return RouterOutput(decision="send_reply") 