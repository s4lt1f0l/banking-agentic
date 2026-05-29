from app.core.schemas import ValidationOutput, DraftOutput

class ValidationNode:
    def execute(self, draft_out: DraftOutput) -> ValidationOutput:
        if len(draft_out.draft_reply) < 15:
            return ValidationOutput(is_valid=False, feedback="Draft response is too short.") #
        
        return ValidationOutput(is_valid=True, feedback="Valid draft.")