# import socket
# import h2.config
# import h2.connection
# import h2.events
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def send_response(conn, h2_conn, event, path):
#     stream_id = event.stream_id
#     print("Sending response for ", path)
#     # conn is the socket connection, h2_conn is the h2 connection, event is the request event and path is the file name
#     # send the file with the name path from the computer1SendFiles folder to the client using the h2 connection and the socket connection conn in chunks
#     with open("../dataFiles/computer1SendFiles/" + path, 'rb') as file:
#         response = file.read()
#     # Send the headers
#     h2_conn.send_headers(stream_id, [(':status', '200'), ('content-length', str(len(response)))])
#     i=1
#     while len(response) > 0:
#         print("Sending chunk ", i)
#         flow_control_window = h2_conn.local_flow_control_window(stream_id)
#         print("Flow control window: ", flow_control_window)
#         frame_size = h2_conn.max_outbound_frame_size
#         print("Frame size: ", frame_size)
#         chunk_size = min(flow_control_window, frame_size)
#         if chunk_size == 0:
#             print("Flow control window is 0")
#             break
#         chunk = response[:chunk_size]
#         response = response[chunk_size:]
#         # Send the chunk and create a header frame
#         h2_conn.send_data(stream_id, chunk)
#         conn.sendall(h2_conn.data_to_send())
#         # Receive the window update from the client
#         # data = conn.recv(65536)
#         # if not data:
#         #     break
#         # events = h2_conn.receive_data(data)
#         # for event in events:
#         #     if isinstance(event, h2.events.WindowUpdated):
#         #         print("Received window update")
#         #         print("Window size: ", event.delta)
#         i+=1

#     # send the end of stream
#     h2_conn.end_stream(event.stream_id)
#     conn.sendall(h2_conn.data_to_send())

# def handle(conn):
#     config = h2.config.H2Configuration(client_side=False, header_encoding='utf-8')
#     h2_conn = h2.connection.H2Connection(config=config)
#     h2_conn.initiate_connection()
#     conn.sendall(h2_conn.data_to_send())

#     while True:
#         data = conn.recv(65536)
#         if not data:
#             break
#         events = h2_conn.receive_data(data)
#         for event in events:
#             if isinstance(event, h2.events.RequestReceived):
#                 for header in event.headers:
#                     if header[0] == ':path':
#                         # path is /file_name extract file_name
#                         path = header[1][1:]
#                 print("Received request for ", path)
#                 send_response(conn, h2_conn, event, path)
#                 print("Sent response for ", path)
                        
#         conn.sendall(h2_conn.data_to_send())


# def main():
#     try:
#         sock = socket.socket()
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         sock.bind((os.getenv('COMP1_IP'), int(os.getenv('PORT'))))
#         print("Server started at ", os.getenv('COMP1_IP'), ":", os.getenv('PORT'), "...")
#         while True:
#             sock.listen(5)
#             conn, addr = sock.accept()
#             print("Connection accepted")
#             handle(conn)
#     finally:
#         sock.close()

# if __name__ == "__main__":
#     main()


import socket
import h2.connection
import h2.config
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_ADDRESS = (os.getenv('COMP1_IP'), int(os.getenv('PORT')))
FILE_FOLDER = '../dataFiles/computer1SendFiles/'

class HTTPServer:
    def __init__(self):
        """Inits the socket, start listening on 8080"""
        print("server starting..")
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(SERVER_ADDRESS)
        self.sock.listen(1)

    def start(self):
        """Start listening to connections"""
        print("server listening for connections..")
        while True:
            self.handle(self.sock.accept()[0])

    def handle(self, sock):
        config = h2.config.H2Configuration(client_side=False)
        conn = h2.connection.H2Connection(config=config)
        conn.initiate_connection()
        sock.sendall(conn.data_to_send())

        headers = {}

        while True:
            data = sock.recv(65535)
            if not data:
                break

            events = conn.receive_data(data)
            for event in events:

                # Recieve and process headers
                if isinstance(event, h2.events.RequestReceived):
                    for _t in event.headers:
                        if _t[0] == ":method":
                            headers["method"] = _t[1]
                        elif _t[0] == ":path":
                            headers["path"] = _t[1]
                    
                    print("Received request for ", headers["path"])

                    # path is /file_name extract file_name
                    file_name = headers["path"][1:]
                    # read the file and send it
                    file_path = FILE_FOLDER + file_name
                    with open(file_path, "rb") as file:
                        response_data = file.read()

                    self.send_successfull_response(conn,sock, event, response_data)
                    print("Sent response for ", headers["path"])


    def send_successfull_response(self, conn,sock, event, response_data):
        """Send a successfull (HTTP 200) response"""

        stream_id = event.stream_id
        conn.send_headers(
            stream_id=stream_id,
            headers=[
                (":status", "200"),
                ("server", "basic-h2-server/1.0"),
                ("content-length", str(len(response_data))),
                ("content-type", "text/html"),
            ],
        )
        sock.sendall(conn.data_to_send())
        for i in range(0, len(response_data), 16384):
            if conn.local_flow_control_window(stream_id) < 16384:
                self.wait_for_window_update(sock, conn)
            conn.send_data(stream_id, response_data[i : i + 16384])
            sock.sendall(conn.data_to_send())
        conn.end_stream(stream_id)
        sock.sendall(conn.data_to_send())

    def wait_for_window_update(self, sock, conn):
        window_updated = False
        while not window_updated:
            # read raw data from the self.socket
            data = sock.recv(65536 * 1024)
            if not data:
                break

            # feed raw data into h2, and process resulting events
            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.WindowUpdated):
                    window_updated = True
        sock.sendall(conn.data_to_send())


if __name__ == "__main__":
    try:
        server = HTTPServer()
        server.start()
    except KeyboardInterrupt:
        server.sock.close()
        print("Server stopped")
        exit(0)