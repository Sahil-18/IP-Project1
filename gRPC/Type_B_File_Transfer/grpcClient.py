import grpc
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import gRPC_transfer_pb2 as pb2
import gRPC_transfer_pb2_grpc as pb2_grpc

import time
from dotenv import load_dotenv
from statistics import mean, stdev

load_dotenv()

SERVER_PATH = os.getenv("COMP2_IP") + ":" + os.getenv("PORT")

def request_file(stub, filename, iteration):
    # Find the total application layer data transferered every time the file is requested including the header and the file data
    RTT = []
    throughput = []
    total_data_transfered = []
    for i in range(iteration):
        print("Requesting file: " + filename + " for the " + str(i+1) + " time")
        if os.path.exists(filename):
            os.remove(filename)
        start = time.time()
        response = stub.GetFile(pb2.FileRequest(filename=filename))
        try:
            with open(filename, 'wb') as file:
                for chunk in response:
                    file.write(chunk.content)
        except FileNotFoundError:
            print("File not found")
        end = time.time()
        print("File received in time: " + str(end - start) + " seconds")
        RTT.append(end - start)
        # File size in bytes
        file_size = os.path.getsize(filename)
        # Throughput in kilo Bytes per second
        # Handle divide by zero error
        if end - start == 0:
            throughput.append(0)
        else:
            throughput.append(file_size * 0.008 / (end - start))
        # total data transfered = header + file size
        total_data_transfered.append((file_size + len(response.initial_metadata()) + len(response.trailing_metadata()))/file_size)
    # Create a csv file to store RTT, throughput and total data transfered with name as filename_results.csv
    with open(filename + "_results.csv", 'w') as file:
        file.write("RTT,Throughput,TotalDataTransfered\n")
        for i in range(iteration):
            file.write(str(RTT[i]) + "," + str(throughput[i]) + "," + str(total_data_transfered[i]) + "\n")

    # Calculate average RTT, throughput and total data transfered also standard Deviation
    # Also ensure that standard deviation is not calculated for 1 iteration
    # Save this in dictionary and return
    results = {}
    results["RTT"] = mean(RTT)
    results["Throughput"] = mean(throughput)
    results["TotalDataTransfered"] = mean(total_data_transfered)
    if iteration != 1:
        results["RTT_Std_Dev"] = stdev(RTT)
        results["Throughput_Std_Dev"] = stdev(throughput)
        results["TotalDataTransfered_Std_Dev"] = stdev(total_data_transfered)
    else:
        results["RTT_Std_Dev"] = 0
        results["Throughput_Std_Dev"] = 0
        results["TotalDataTransfered_Std_Dev"] = 0
    return results

def run_client():
    channel = grpc.insecure_channel(SERVER_PATH)
    stub = pb2_grpc.FileTransferStub(channel)
    
    # Request A_10kB file 1000 times
    result_B_10kB = request_file(stub, "B_10KB", 10000)
    # Request A_100KB file 100 times
    result_B_100kB = request_file(stub, "B_100KB", 1000)
    # Request A_1MB file 10 times
    result_B_1MB = request_file(stub, "B_1MB", 10)
    # Request A_10MB file 1 time
    result_B_10MB = request_file(stub, "B_10MB", 1)

    print("\nResults for B_10KB file")
    print(result_B_10kB)

    print("\nResults for B_100KB file")
    print(result_B_100kB)

    print("\nResults for B_1MB file")
    print(result_B_1MB)

    print("\nResults for B_10MB file")
    print(result_B_10MB)

if __name__ == "__main__":
    run_client()