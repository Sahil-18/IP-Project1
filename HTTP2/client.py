# from hyper import HTTP20Connection
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def request_and_save(connection, file_path):
#     stream = connection.request('GET', '/' + file_path)
#     print("Requested", file_path)
#     # Accept stream of data from server
#     response = connection.get_response(stream)
#     # Data is received as a stream of chunks
#     # Save the data to a file
#     for chunk in response.read_chunked(decode_content=True):
#         with open(file_path + '_', 'ab') as file:
#             print("Received chunk")
#             file.write(chunk)
          
#             # Send acknowledgement with updated flow control window to server
#             # connection.window_manager.increment_flow_control(65536)



# def make_request():
#     # Make an HTTP/2.0 request to the server for the specified file
#     connection = HTTP20Connection(os.getenv('COMP1_IP'), port=int(os.getenv('PORT')))
#     print(connection)
#     # for _ in range(1):
#     #     print("Requesting A_10kB")
#     #     request_and_save(connection, 'A_10kB')
#     #     print("Received A_10kB")
    
#     for _ in range(1):
#         print("Requesting A_100kB")
#         request_and_save(connection, 'A_100kB')
#         print("Received A_100kB")

#     # for _ in range(1):
#     #     print("Requesting A_1MB")
#     #     request_and_save(connection, 'A_1MB')
#     #     print("Received A_1MB")

#     # for _ in range(1):
#     #     print("Requesting A_10MB")
#     #     request_and_save(connection, 'A_10MB')
#     #     print("Received A_10MB")

#     connection.close()

# if __name__ == "__main__":
#     make_request()

import socket
import h2.connection
import h2.config
import h2.events
import socket
import sys


class HTTPClient:
    """Client for the http connection and requests"""

    def __init__(self, server, port):

        self.SERVER_NAME = server
        self.SERVER_PORT = port

    def open_connection(self):
        """Open a connection to the server"""
        socket.setdefaulttimeout(15)

        # open a socket to the server
        self.socket = socket.create_connection((self.SERVER_NAME, self.SERVER_PORT))

        self.connection = h2.connection.H2Connection()
        self.connection.initiate_connection()
        self.socket.sendall(self.connection.data_to_send())


    def send_request(self, headers):
        self.open_connection()
        response = self.__send_request(headers, 1)
        self.close_connection()

        return response

    def __send_request(self, headers_to_send, stream_id):
        if headers_to_send:
            self.connection.send_headers(stream_id, headers_to_send)
            self.socket.sendall(self.connection.data_to_send())

        response_stream_ended = False
        received_data = b""
        while not response_stream_ended:
            data = self.socket.recv(65536 * 1024)
            if not data:
                break

            events = self.connection.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.DataReceived):                    
                    received_data += event.data

                    self.connection.acknowledge_received_data(
                        event.flow_controlled_length, event.stream_id
                    )

                if isinstance(event, h2.events.StreamEnded):
                    response_stream_ended = True
                    break
            self.socket.sendall(self.connection.data_to_send())

        return received_data

    def wait_for_window_update(self):
        window_updated = False
        while not window_updated:
            data = self.socket.recv(65536 * 1024)
            if not data:
                break

            events = self.connection.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.WindowUpdated):
                    window_delta = event.delta
                    window_updated = True

            self.socket.sendall(self.connection.data_to_send())

        return window_delta

    def close_connection(self):
        self.connection.close_connection()
        self.socket.sendall(self.connection.data_to_send())
        self.socket.close()


client = HTTPClient("localhost", 8000)
headers = [
    (":method", "GET"),
    (":path", "/A_10MB"),
    (":authority", "localhost"),
    (":scheme", "https"),
]

response = client.send_request(headers)
# save the response to a file
with open("A_100KB_", "wb") as file:
    file.write(response)