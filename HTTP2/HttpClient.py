# import asyncio
# import h2.connection
# import socket
# import time

# def create_connection():
#     sock = socket.create_connection(('10.154.51.139', 8889))
#     return h2.connection.H2Connection(client_side=True), sock.makefile('rwb', buffering=0)

# def send_request(connection, stream_id, method, path):
#     headers = [
#         (':method', method),
#         (':path', path),
#         (':authority', '10.154.51.139:8889'),
#         (':scheme', 'http'),
#     ]
#     connection.send_headers(stream_id, headers, end_stream=True)

# def receive_response(connection):
#     response_data = b""
#     while True:
#         frame = connection.recv_data(65536)
#         if frame is None:
#             break
#         response_data += frame
#     return response_data

# def save_response_to_file(file_path, response_data):
#     with open(file_path, 'wb') as file:
#         file.write(response_data)

# def request_and_save(file_path, method, path):
#     connection, sock = create_connection()
#     connection.initiate_connection()
#     sock.write(connection.data_to_send())

#     stream_id = connection.get_next_available_stream_id()
#     send_request(connection, stream_id, method, path)
#     sock.write(connection.data_to_send())

#     time.sleep(1)  # Simulate delay for receiving the response

#     response_data = receive_response(connection)
#     save_response_to_file(file_path, response_data)

#     sock.close()

# async def main():
#     # Experiment 1
#     for _ in range(1000):
#         request_and_save('A_10kB_from_server.txt', 'GET', '/A_10kB')
#         request_and_save('B_1kB_from_server.txt', 'GET', '/B_1kB')

#     # Experiment 2
    # for _ in range(100):
    #     request_and_save('A_100kB_from_server.txt', 'GET', '/A_100kB')
    #     request_and_save('B_10kB_from_server.txt', 'GET', '/B_10kB')

# Experiment 2
from hyper import HTTP20Connection
from dotenv import load_dotenv
import os

load_dotenv()

def request_and_save(connection, file_path):
    stream = connection.request('GET', '/' + file_path)
    print("Requested", file_path)
    # Accept stream of data from server
    response = connection.get_response(stream)
    print(response.headers)
    print(response.read())

    # response = connection.get_response()
    # print(response.headers)
    # response_data = None
    # for chunk in response.stream():
    #     if chunk is not None:
    #         response_data += chunk
    #     else:
    #         break
    # with open(file_path, 'wb') as file:
    #     file.write(response_data)

def make_request():
    # Make an HTTP/2.0 request to the server for the specified file
    connection = HTTP20Connection(os.getenv('COMP1_IP'), port=int(os.getenv('PORT')))
    print(connection)
    # for _ in range(1):
    #     print("Requesting A_10kB")
    #     request_and_save(connection, 'A_10kB')
    #     print("Received A_10kB")
    
    for _ in range(1):
        print("Requesting A_100kB")
        request_and_save(connection, 'A_100kB')
        print("Received A_100kB")

    # for _ in range(1):
    #     print("Requesting A_1MB")
    #     request_and_save(connection, 'A_1MB')
    #     print("Received A_1MB")

    # for _ in range(1):
    #     print("Requesting A_10MB")
    #     request_and_save(connection, 'A_10MB')
    #     print("Received A_10MB")

    connection.close()

if __name__ == "__main__":
    make_request()
