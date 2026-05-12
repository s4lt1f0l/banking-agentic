#
from app.core.schemas import CustomerRequest, AgentResponse, WorkflowTrace
from app.nodes.intent_node import IntentDetectionNode
from app.nodes.priority_node import PriorityDetectionNode
from app.nodes.policy_node import PolicyRetrievalNode
from app.nodes.draft_node import ResponseDraftingNode
from app.nodes.validation_node import ValidationNode
from app.nodes.router_node import RouterNode

class BankingAgentOrchestrator:
    def __init__(self):
        self.intent_node = IntentDetectionNode()
        self.priority_node = PriorityDetectionNode()
        self.policy_node = PolicyRetrievalNode()
        self.draft_node = ResponseDraftingNode()
        self.validation_node = ValidationNode()
        self.router_node = RouterNode()

    def process_request(self, request: CustomerRequest) -> AgentResponse:
        trace = WorkflowTrace(request=request) #

        # 1. Intent detection
        trace.intent_detection = self.intent_node.execute(request.message)

        # 2. Priority detection
        trace.priority_assessment = self.priority_node.execute(request.message, trace.intent_detection.intent)

        # 3. Policy retrieval
        trace.policy_retrieval = self.policy_node.execute(trace.intent_detection.intent)

        # 4. Response drafting
        trace.response_drafting = self.draft_node.execute(
            request, trace.intent_detection, trace.priority_assessment, trace.policy_retrieval
        )

        # 5. Validation
        trace.validation = self.validation_node.execute(trace.response_drafting)

        # 6. Routing
        trace.final_routing = self.router_node.execute(
            trace.priority_assessment, trace.validation, trace.response_drafting
        )

        final_reply = None
        if trace.final_routing.decision in ["send_reply", "ask_info"]: #
            final_reply = trace.response_drafting.draft_reply

        return AgentResponse(
            decision=trace.final_routing.decision, #
            final_reply=final_reply,
            trace=trace #
        )