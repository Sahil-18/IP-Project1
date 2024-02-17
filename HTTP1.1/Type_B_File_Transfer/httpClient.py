import http.client  
import sys  
from statistics import mean, stdev
import time
import os
from dotenv import load_dotenv
load_dotenv()

SERVER_PATH = (os.getenv("COMP2_IP"), int(os.getenv("PORT")))
conn = http.client.HTTPConnection(SERVER_PATH) 
 
def downloadfile(file:str, repeat: int):
    sizes = []
    thptvalues = []
    print(f"##### Sending Request to Server for: {file} --{repeat} times #####")
    print("Getting the files ....")
    for _ in range(repeat):
        if os.path.exists(file):
            os.remove(file)
        start_time = time.time()
        conn.request("GET", file)
        #open  file to write contents 
        f = open(file, 'wb+')        
        rsp = conn.getresponse()  
        #print server response and data  
        #print(rsp.status, rsp.reason)    
        data_received = rsp.read()  
        f.write(data_received)
        timetaken = time.time() - start_time
        size = os.path.getsize(file)
        #throughput after each file transfer
        thpt = size * 0.008 / timetaken
        thptvalues.append(thpt)
        #sizes.append(len(data_received))
        
        header_size =len(rsp.headers.as_bytes())
        #total received data = headers received(header_size)+ status line(18)
        applayersize=(header_size+size+18+len(rsp.headers))/size        
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


if __name__ == "__main__":
    # Downlink 100 B file
    print("Downloading B_10kB file")
    result_B_10kB = downloadfile("B_10kB", 1)
    
    # # Downlink 10kB file
    print("Downloading B_100kB file")
    result_B_100kB = downloadfile("B_100kB", 100)

    # # Downlink 1MB file
    print("Downloading B_1MB file")
    result_B_1MB = downloadfile("B_1MB", 10)

    # Downlink 10MB file
    print("Downloading B_10MB file")
    result_B_10MB = downloadfile("B_10MB", 1)
    conn.close()

    print("\nResults for B_10KB file")
    print(result_B_10kB)

    print("\nResults for B_100KB file")
    print(result_B_100kB)

    print("\nResults for B_1MB file")
    print(result_B_1MB)

    print("\nResults for A_10MB file")
    print(result_B_10MB)
    
    