import grpc
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import gRPC_transfer_pb2 as pb2
import gRPC_transfer_pb2_grpc as pb2_grpc

from dotenv import load_dotenv
from concurrent import futures

load_dotenv()

SERVER_ADDRESS = os.getenv("COMP1_IP") + ":" + os.getenv("PORT")
FILE_FOLDER = os.getenv("A_FILES_LOCATION")

class FileTransferServicer(pb2_grpc.FileTransferServicer):
    def GetFile(self, request, context):
        filename = request.filename
        print("\nRequest for file: " + filename)
        file_path = FILE_FOLDER + filename
        try:
            print("Sending file: " + filename)
            chunk_size = 1024*1024
            with open(file_path, 'rb') as file:
                while True:
                    content = file.read(chunk_size)
                    if not content:
                        break
                    yield pb2.FileResponse(content=content)
            print("File sent successfully")
        except FileNotFoundError:
            context.set_details("File not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return pb2.FileResponse()
        
def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    print("Server started at " + SERVER_ADDRESS)
    server.wait_for_termination()

if __name__ == "__main__":
    run()