import socket
import h2.config
import h2.connection
import h2.events

def send_response(conn, event, path):
    stream_id = event.stream_id
    filePath = "../dataFiles/computer1SendFiles/" + path
    print(filePath)
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
    conn.send_data(
        stream_id=stream_id,
        data=response_data,
        end_stream=True
    )
    

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
                send_response(h2_conn, event, path)
                        
        conn.sendall(h2_conn.data_to_send())


def main():
    try:
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 8889))
        print("Server started")
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