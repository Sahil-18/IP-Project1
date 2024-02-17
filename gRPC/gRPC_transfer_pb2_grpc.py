# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gRPC_transfer_pb2 as gRPC__transfer__pb2


class FileTransferStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFile = channel.unary_stream(
                '/FileTransfer/GetFile',
                request_serializer=gRPC__transfer__pb2.FileRequest.SerializeToString,
                response_deserializer=gRPC__transfer__pb2.FileResponse.FromString,
                )


class FileTransferServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileTransferServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFile': grpc.unary_stream_rpc_method_handler(
                    servicer.GetFile,
                    request_deserializer=gRPC__transfer__pb2.FileRequest.FromString,
                    response_serializer=gRPC__transfer__pb2.FileResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'FileTransfer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileTransfer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/FileTransfer/GetFile',
            gRPC__transfer__pb2.FileRequest.SerializeToString,
            gRPC__transfer__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
