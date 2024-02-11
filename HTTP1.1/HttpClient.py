import http.client  
import sys  
from statistics import mean, stdev
import time

conn = http.client.HTTPConnection('10.152.16.75', 8889)  
 
def downloadfile(file:str, repeat: int, size: int):
    sizes = []
    thptvalues = []
    print(f"##### Sending Request to Server for: {file} --{repeat} times #####")
    print("Getting the files ....")
    for _ in range(repeat):
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
        #throughput after each file transfer
        thpt = size * 0.008 / timetaken
        thptvalues.append(thpt)
        #sizes.append(len(data_received))
        
        header_size =len(rsp.headers.as_bytes())
        #total received data = headers received(header_size)+ status line(18)
        applayersize=(header_size+size+18+len(rsp.headers))/size        
        sizes.append(applayersize)

    print(f"##### File download complete for: {file} #####")
    print(file, "Average throughput in kilobits per second :",mean(thptvalues))
    # print(file, "Throughput Standard Deviation in kilobits per second :",stdev(thptvalues))
    print(file, "Average Application Layer data received per file size:", mean(sizes))
    print("\n")
    


if __name__ == "__main__":
    # Downlink 100 B file
    print("Downloading 100B file")
    downloadfile("A_100KB", 1, 102400)
    
    # # Downlink 10kB file
    print("Downloading 10KB file")
    downloadfile("A_10KB", 1, 10240)

    # # Downlink 1MB file
    print("Downloading 1MB file")
    downloadfile("A_1MB", 1, 1048576)

    # Downlink 10MB file
    print("Downloading 10MB file")
    downloadfile("A_10MB", 1, 10485760)
    conn.close()
    