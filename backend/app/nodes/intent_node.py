from app.clients.grpc_intent_client import GrpcIntentClient
from app.core.schemas import IntentOutput

class IntentDetectionNode:
    def __init__(self):
        self.client = GrpcIntentClient()

    def execute(self, message: str) -> IntentOutput:
        return self.client.recognize(message)
