# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gRPC_transfer.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13gRPC_transfer.proto\"\x1f\n\x0b\x46ileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"\x1f\n\x0c\x46ileResponse\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\x0c\x32\x38\n\x0c\x46ileTransfer\x12(\n\x07GetFile\x12\x0c.FileRequest\x1a\r.FileResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gRPC_transfer_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FILEREQUEST']._serialized_start=23
  _globals['_FILEREQUEST']._serialized_end=54
  _globals['_FILERESPONSE']._serialized_start=56
  _globals['_FILERESPONSE']._serialized_end=87
  _globals['_FILETRANSFER']._serialized_start=89
  _globals['_FILETRANSFER']._serialized_end=145
# @@protoc_insertion_point(module_scope)
