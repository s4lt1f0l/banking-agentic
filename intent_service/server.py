from concurrent import futures

import grpc

import intent_service_pb2
import intent_service_pb2_grpc
from classifier import IntentClassifier
from settings import settings


class IntentService(intent_service_pb2_grpc.IntentServiceServicer):
    def __init__(self):
        self.classifier = IntentClassifier()

    def IntentRecognizer(self, request, context):
        intent, confidence, reason = self.classifier.classify(request.message)
        return intent_service_pb2.IntentResponse(
            intent=intent,
            confidence=confidence,
            reason=reason,
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intent_service_pb2_grpc.add_IntentServiceServicer_to_server(IntentService(), server)
    server.add_insecure_port(f"[::]:{settings.GRPC_PORT}")
    server.start()
    print(f"Intent service listening on {settings.GRPC_PORT}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
