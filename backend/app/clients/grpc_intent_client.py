import grpc

from app.clients.intent_grpc import intent_service_pb2, intent_service_pb2_grpc
from app.core.schemas import IntentOutput
from app.core.settings import settings


class GrpcIntentClient:
    def __init__(self):
        target = f"{settings.INTENT_SERVICE_HOST}:{settings.INTENT_SERVICE_PORT}"
        self.channel = grpc.insecure_channel(target)
        self.stub = intent_service_pb2_grpc.IntentServiceStub(self.channel)

    def recognize(self, message: str) -> IntentOutput:
        try:
            request = intent_service_pb2.IntentRequest(message=message)
            response = self.stub.IntentRecognizer(
                request,
                timeout=settings.INTENT_SERVICE_TIMEOUT,
            )
            return IntentOutput(
                intent=response.intent or "default",
                confidence=float(response.confidence),
                reason=response.reason or None,
            )
        except grpc.RpcError as exc:
            return IntentOutput(
                intent="default",
                confidence=0.0,
                reason=f"Intent service error: {exc.code().name}",
            )
