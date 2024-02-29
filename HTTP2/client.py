import socket
import h2.connection
import h2.config
import h2.events
from statistics import mean, stdev
import time
import os
from dotenv import load_dotenv

load_dotenv()


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


    def send_request(self, file, repeat):
        sizes = []
        thptvalues = []
        print(f"##### Sending Request to Server for: {file} --{repeat} times #####")
        print("Getting the files ....")

        for _ in range(repeat):
            if os.path.exists(file):
                os.remove(file)
            start = time.time()
            headers_to_send = [
                (":method", "GET"),
                (":scheme", "http"),
                (":authority", self.SERVER_NAME),
                (":path", "/" + file),
                ("accept", "text/html"),
            ]
            stream_id = 1
            if headers_to_send:
                self.connection.send_headers(stream_id, headers_to_send)
                self.socket.sendall(self.connection.data_to_send())

            response_stream_ended = False
            header_len = 0
            received_data = b""
            while not response_stream_ended:
                data = self.socket.recv(65536 * 1024)
                if not data:
                    break

                events = self.connection.receive_data(data)
                for event in events:
                    if isinstance(event, h2.events.ResponseReceived):
                        header_len = len(event.headers)
                    if isinstance(event, h2.events.DataReceived):                   
                        received_data += event.data

                        self.connection.acknowledge_received_data(
                            event.flow_controlled_length, event.stream_id
                        )

                    if isinstance(event, h2.events.StreamEnded):
                        response_stream_ended = True
                        break
                self.socket.sendall(self.connection.data_to_send())
            end = time.time()
            # Save the file
            with open(file, "wb") as f:
                f.write(received_data)
            time_taken = end - start
            if time_taken == 0:
                time_taken = 0.0001
            size = os.path.getsize(file)
            thpt = size * 0.008 / time_taken
            thptvalues.append(thpt)
            applayersize = (header_len + size + 18)
            sizes.append(applayersize)
        
        # Create a csv file to store RTT, throughput and total data transfered with name as filename_results.csv
        with open(file + "_results.csv", 'w') as file:
            file.write("RTT,Throughput,TotalDataTransfered\n")
            for i in range(repeat):
                file.write(str(sizes[i]) + "," + str(thptvalues[i]) + "," + str(sizes[i]) + "\n")

        # Calculate average RTT, throughput and total data transfered also standard Deviation
        # Also ensure that standard deviation is not calculated for 1 iteration
        # Save this in dictionary and return
                
        results = {}
        results["RTT"] = mean(sizes)
        results["Throughput"] = mean(thptvalues)
        results["TotalDataTransfered"] = mean(sizes)
        if repeat > 1:
            results["RTT_Std_Dev"] = stdev(sizes)
            results["Throughput_Std_Dev"] = stdev(thptvalues)
            results["TotalDataTransfered_Std_Dev"] = stdev(sizes)
        else:
            results["RTT_Std_Dev"] = 0
            results["Throughput_Std_Dev"] = 0
            results["TotalDataTransfered_Std_Dev"] = 0
        return results


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


if __name__ == "__main__":
    client = HTTPClient(os.getenv("COMP1_IP"), int(os.getenv("PORT")))
    client.open_connection()

    # Request A_10kB file for 1000 times
    print("Downloading A_10kB file")
    result_A_10kB = client.send_request("A_10kB", 1000)
    
    # # Downlink 10kB file
    print("Downloading A_100kB file")
    result_A_100kB = client.send_request("A_100kB", 100)

    # # Downlink 1MB file
    print("Downloading A_1MB file")
    result_A_1MB = client.send_request("A_1MB", 10)

    # Downlink 10MB file
    print("Downloading A_10MB file")
    result_A_10MB = client.send_request("A_10MB", 1)

    client.close_connection()
    
    print("\nResults for A_10KB file")
    print(result_A_10kB)

    print("\nResults for A_100KB file")
    print(result_A_100kB)

    print("\nResults for A_1MB file")
    print(result_A_1MB)

    print("\nResults for A_10MB file")
    print(result_A_10MB)


    
