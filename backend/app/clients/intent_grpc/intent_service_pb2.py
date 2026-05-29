# Generated-compatible protobuf definitions for intent_service.proto.
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()

_file_proto = _descriptor_pb2.FileDescriptorProto()
_file_proto.name = "intent_service.proto"
_file_proto.package = "intent_classify.v1"
_file_proto.syntax = "proto3"

_intent_request = _file_proto.message_type.add()
_intent_request.name = "IntentRequest"
_field = _intent_request.field.add()
_field.name = "message"
_field.number = 1
_field.label = _descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = _descriptor_pb2.FieldDescriptorProto.TYPE_STRING

_intent_response = _file_proto.message_type.add()
_intent_response.name = "IntentResponse"
_field = _intent_response.field.add()
_field.name = "intent"
_field.number = 1
_field.label = _descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = _descriptor_pb2.FieldDescriptorProto.TYPE_STRING
_field = _intent_response.field.add()
_field.name = "confidence"
_field.number = 2
_field.label = _descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = _descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT
_field = _intent_response.field.add()
_field.name = "reason"
_field.number = 3
_field.label = _descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = _descriptor_pb2.FieldDescriptorProto.TYPE_STRING

_service = _file_proto.service.add()
_service.name = "IntentService"
_method = _service.method.add()
_method.name = "IntentRecognizer"
_method.input_type = ".intent_classify.v1.IntentRequest"
_method.output_type = ".intent_classify.v1.IntentResponse"

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(_file_proto.SerializeToString())

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "intent_service_pb2", globals())

_sym_db.RegisterMessage(IntentRequest)
_sym_db.RegisterMessage(IntentResponse)
