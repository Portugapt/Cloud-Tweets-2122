# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tweetMessages.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13tweetMessages.proto\"9\n\x13TimeIntervalRequest\x12\x11\n\tstartTime\x18\x01 \x01(\t\x12\x0f\n\x07\x65ndTime\x18\x02 \x01(\t\"5\n\x0eSpokenLanguage\x12\x10\n\x08language\x18\x01 \x01(\t\x12\x11\n\tfrequency\x18\x02 \x01(\x05\"I\n\x1alistSpokenLanguageResponse\x12+\n\x12listSpokenLanguage\x18\x01 \x03(\x0b\x32\x0f.SpokenLanguage\"/\n\x08Location\x12\x10\n\x08location\x18\x01 \x01(\t\x12\x11\n\tfrequency\x18\x02 \x01(\x05\"7\n\x14listLocationResponse\x12\x1f\n\x0clistLocation\x18\x01 \x03(\x0b\x32\t.Locationb\x06proto3')



_TIMEINTERVALREQUEST = DESCRIPTOR.message_types_by_name['TimeIntervalRequest']
_SPOKENLANGUAGE = DESCRIPTOR.message_types_by_name['SpokenLanguage']
_LISTSPOKENLANGUAGERESPONSE = DESCRIPTOR.message_types_by_name['listSpokenLanguageResponse']
_LOCATION = DESCRIPTOR.message_types_by_name['Location']
_LISTLOCATIONRESPONSE = DESCRIPTOR.message_types_by_name['listLocationResponse']
TimeIntervalRequest = _reflection.GeneratedProtocolMessageType('TimeIntervalRequest', (_message.Message,), {
  'DESCRIPTOR' : _TIMEINTERVALREQUEST,
  '__module__' : 'tweetMessages_pb2'
  # @@protoc_insertion_point(class_scope:TimeIntervalRequest)
  })
_sym_db.RegisterMessage(TimeIntervalRequest)

SpokenLanguage = _reflection.GeneratedProtocolMessageType('SpokenLanguage', (_message.Message,), {
  'DESCRIPTOR' : _SPOKENLANGUAGE,
  '__module__' : 'tweetMessages_pb2'
  # @@protoc_insertion_point(class_scope:SpokenLanguage)
  })
_sym_db.RegisterMessage(SpokenLanguage)

listSpokenLanguageResponse = _reflection.GeneratedProtocolMessageType('listSpokenLanguageResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSPOKENLANGUAGERESPONSE,
  '__module__' : 'tweetMessages_pb2'
  # @@protoc_insertion_point(class_scope:listSpokenLanguageResponse)
  })
_sym_db.RegisterMessage(listSpokenLanguageResponse)

Location = _reflection.GeneratedProtocolMessageType('Location', (_message.Message,), {
  'DESCRIPTOR' : _LOCATION,
  '__module__' : 'tweetMessages_pb2'
  # @@protoc_insertion_point(class_scope:Location)
  })
_sym_db.RegisterMessage(Location)

listLocationResponse = _reflection.GeneratedProtocolMessageType('listLocationResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTLOCATIONRESPONSE,
  '__module__' : 'tweetMessages_pb2'
  # @@protoc_insertion_point(class_scope:listLocationResponse)
  })
_sym_db.RegisterMessage(listLocationResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TIMEINTERVALREQUEST._serialized_start=23
  _TIMEINTERVALREQUEST._serialized_end=80
  _SPOKENLANGUAGE._serialized_start=82
  _SPOKENLANGUAGE._serialized_end=135
  _LISTSPOKENLANGUAGERESPONSE._serialized_start=137
  _LISTSPOKENLANGUAGERESPONSE._serialized_end=210
  _LOCATION._serialized_start=212
  _LOCATION._serialized_end=259
  _LISTLOCATIONRESPONSE._serialized_start=261
  _LISTLOCATIONRESPONSE._serialized_end=316
# @@protoc_insertion_point(module_scope)
