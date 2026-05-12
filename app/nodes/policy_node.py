from app.core.schemas import PolicyOutput
from app.data.policies import get_policy_for_intent #

class PolicyRetrievalNode:
    def execute(self, intent: str) -> PolicyOutput:
        policy = get_policy_for_intent(intent) #
        return PolicyOutput(policy_text=policy)