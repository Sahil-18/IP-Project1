import socket
import h2.config
import h2.connection
import h2.events
from dotenv import load_dotenv
import os

load_dotenv()

def send_response(conn, h2_conn, event, path):
    stream_id = event.stream_id
    # conn is the socket connection, h2_conn is the h2 connection, event is the request event and path is the file name
    # send the file with the name path from the computer1SendFiles folder to the client using the h2 connection and the socket connection conn in chunks
    with open("../dataFiles/computer1SendFiles/" + path, 'rb') as file:
        response = file.read()
    
    h2_conn.send_headers(
        stream_id=event.stream_id,
        headers=[
            (':status', '200'),
            ('content-length', str(len(response))),
        ],
    )
    # Cannot send the whole file at once, so send in chunks
    # chunk size is the minimum of flow control window and the frame size
    # flow control window is the minimum of the connection flow control window and the stream flow control window

    # get the flow control window for the connection and the stream
    connection_flow_control_window = h2_conn.local_flow_control_window(stream_id=stream_id)
    stream_flow_control_window = h2_conn.local_flow_control_window(stream_id=event.stream_id)

    # get the frame size
    frame_size = h2_conn.max_outbound_frame_size
    # send the file in chunks
    while len(response) > 0:
        # get the chunk size
        chunk_size = min(min(connection_flow_control_window, stream_flow_control_window), frame_size)
        # send the chunk
        h2_conn.send_data(event.stream_id, response[:chunk_size])
        conn.sendall(h2_conn.data_to_send())
        response = response[chunk_size:]

    # send the end of stream
    h2_conn.end_stream(event.stream_id)
    conn.sendall(h2_conn.data_to_send())

def handle(conn):
    config = h2.config.H2Configuration(client_side=False, header_encoding='utf-8')
    h2_conn = h2.connection.H2Connection(config=config)
    h2_conn.initiate_connection()
    conn.sendall(h2_conn.data_to_send())

    while True:
        data = conn.recv(65536)
        if not data:
            break
        events = h2_conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.RequestReceived):
                for header in event.headers:
                    if header[0] == ':path':
                        # path is /file_name extract file_name
                        path = header[1][1:]
                print("Received request for ", path)
                send_response(conn, h2_conn, event, path)
                print("Sent response for ", path)
                        
        conn.sendall(h2_conn.data_to_send())


def main():
    try:
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((os.getenv('COMP1_IP'), int(os.getenv('PORT'))))
        print("Server started at ", os.getenv('COMP1_IP'), ":", os.getenv('PORT'), "...")
        while True:
            sock.listen(5)
            conn, addr = sock.accept()
            print("Connection accepted")
            handle(conn)
    finally:
        sock.close()

if __name__ == "__main__":
    main()


# import asyncio
# import h2.connection
# import h2.events
# from h2.config import H2Configuration

# class HTTP2RequestHandler:
#     def __init__(self, conn):
#         self.conn = conn

#     async def handle(self, reader, writer):
#         config = H2Configuration(client_side=False, header_encoding='utf-8')
#         h2_conn = h2.connection.H2Connection(config=config)
#         h2_conn.initiate_connection()
#         writer.write(h2_conn.data_to_send())

#         while True:
#             data = await reader.read(65536)
#             if not data:
#                 break
#             events = h2_conn.receive_data(data)
#             for event in events:
#                 if isinstance(event, h2.events.RequestReceived):
#                     if event.headers:
#                         for header in event.headers:
#                             if header[0] == ':path':
#                                 path = header[1][1:]
#                                 with open("../dataFiles/computer1SendFiles/" + path, 'rb') as file:
#                                     response = file.read()
#                         print("Sending file ", path, " of size ", len(response))
#                         print("Sending File from path : ../dataFiles/computer1SendFiles/" + path)
#                         h2_conn.send_headers(
#                             stream_id=event.stream_id,
#                             headers=[
#                                 (':status', '200'),
#                                 ('content-length', str(len(response))),
#                             ],
#                         )
#                         h2_conn.send_data(stream_id=event.stream_id, data=response)
#             writer.write(h2_conn.data_to_send())
#             print("Data sent")
#             await writer.drain()


# async def main():
#     server = await asyncio.start_server(
#         lambda r, w: HTTP2RequestHandler(h2.connection.H2Connection(config=H2Configuration(client_side=True))).handle(r, w),
#         host='127.0.0.1',
#         port=8889
#     )

#     print("Server started")
#     async with server:
#         await server.serve_forever()

# asyncio.run(main())