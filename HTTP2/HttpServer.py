import socket
import h2.config
import h2.connection
import h2.events
from dotenv import load_dotenv
import os

load_dotenv()

def send_response(conn, event, path):
    stream_id = event.stream_id
    filePath = "../dataFiles/computer1SendFiles/" + path
    with open(filePath, 'rb') as file:
        response_data = file.read()

    conn.send_headers(
        stream_id=stream_id,
        headers=[
            (':status', '200'),
            ('server', 'basic-h2-server/1.0'),
            ('content-length', str(len(response_data))),
            ('content-type', 'text/plain'),
        ],
    )
    # conn.send_data(
    #     stream_id=stream_id,
    #     data=response_data,
    #     end_stream=True
    # )
    print("Max outbound frame size: ", conn.max_outbound_frame_size)
    print("Local flow control window: ", conn.local_flow_control_window(stream_id))
    chunk_size = min(conn.max_outbound_frame_size, conn.local_flow_control_window(stream_id))
    # chunk_size = 1024
    i = 0
    while response_data:
        chunk = response_data[:chunk_size]
        response_data = response_data[chunk_size:]
        if not response_data:
            conn.send_data(
                stream_id=stream_id,
                data=chunk,
                end_stream=True)
            break
        conn.send_data(
            stream_id=stream_id,
            data=chunk,
            end_stream=False)
        print("Sent chunk  ", i)
        i += 1
        print("Max outbound frame size: ", conn.max_outbound_frame_size)
        print("Local flow control window: ", conn.local_flow_control_window(stream_id))
        # if local flow control window is 0, wait for it to be updated
        while conn.local_flow_control_window(stream_id) < conn.max_outbound_frame_size:
            pass
        chunk_size = min(conn.max_outbound_frame_size, conn.local_flow_control_window(stream_id))
    conn.end_stream(stream_id)
    

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
                send_response(h2_conn, event, path)
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