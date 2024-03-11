# IP-Project1
Internet Protocols Project 1 - CSC 573 Spring 2024

## Team Members

#### 1. Sahil Purohit (spurohi2)
#### 2. Shivangi Chopra (schopra4)


## Project Description and File Structure
Project is implementation of multiple protocols to transfer files of various size from one computer to another. The protocols implemented are:
1. HTTP 1.1
2. HTTP 2.0
3. gRPC
4. BitTorrent

Project file structure is as follows:
1. Three folders for each client-server type protocol: HTTP1.1, HTTP2.0, gRPC. Each folder contains two more folders: Type_A_File_Transfer and Type_B_File_Transfer. Each of these folders contains server and client code.
2. BitTorrent folder contains seeder and leecher code.
3. dataFiles folder: This folde further contains two folders: computer1SendFiles and computer2ReceivedFiles. computer1SendFiles contains files to be sent (A Type Files) from computer 1 and computer2ReceivedFiles contains files to be sent (B Type Files) from computer 2.
4. .env file: This file contains the IP address and port number of the server and client for each protocol. This file is used to set the environment variables for the server and client code.
5. README.md: This file contains the project description and file structure and instructions to run the code.
6. requirements.txt: This file contains the list of all the dependencies required to run the code.

## Instructions to run the code
### 1. Running Client-Server Protocols like: HTTP, gRPC
- Note: This code is tested on Windows machine and not on Linux or Mac. So, we recommend to run the code on Windows machine. All the instructions are for Windows machine.
- Install the dependencies using the following command:
    ```
    pip install -r requirements.txt
    ```
- You can also install the dependencies using the following command or using the link provided below:
    ```
    pip install grpcio
    pip install grpcio-tools
    pip install http
    pip install h2
    pip install python-dotenv
    pip install timeit
    ```
- [h2](https://pypi.org/project/h2/)
- [http](https://pypi.org/project/http/)
- [grpcio](https://pypi.org/project/grpcio/)
- [grpcio-tools](https://pypi.org/project/grpcio-tools/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [timeit](https://pypi.org/project/timeit/)

- Set the environment variables in the .env file. The .env file contains the IP address and port number of the server and client for each protocol.
    ```
    COMP1_IP = IP address of the computer 1
    COMP2_IP = IP address of the computer 2
    PORT = Port number used by server
    A_FILES_LOCATION = Relative path of the folder containing A type files
    B_FILES_LOCATION = Relative path of the folder containing B type files
    ```
- For Type A File Transfer:
    - In the terminal, navigate to the folder containing the  code.
    - The computer 1 whose IP address is set to variable COMP1_IP in .env file should run the server code and computer 2 whose IP address is set to variable COMP2_IP in .env file should run the client code using the following command:
        ```
        python ****server.py
        python ****client.py
        ```
    - The * here represents the protocol name. For example, for HTTP1.1, the command will be:
        ```
        python httpServer.py
        python httpClient.py
        ```
- For Type B File Transfer:
    - In the terminal, navigate to the folder containing the  code.
    - The computer 2 whose IP address is set to variable COMP2_IP in .env file should run the server code and computer 1 whose IP address is set to variable COMP1_IP in .env file should run the client code using the following command:
        ```
        python ****server.py
        python ****client.py
        ```
    - The * here represents the protocol name. For example, for HTTP1.1, the command will be:
        ```
        python httpServer.py
        python httpClient.py
        ```
### 2. Running BitTorrent
- Note: This code is tested on linux machine and not on Windows or Mac. So, we recommend to run the code on linux machine. All the instructions are for linux machine.
- Install the dependencies using the following command:
    ```
    sudo apt install libtorrent
    sudo apt install python-libtorrent
    ```
- Install a library to create a .torrent file which is shared to all the peers.
    ```
    pip3 install py3createtorrent
    ```
    This will create a torrent file (eg : A_10kB.torrent) that is sent to the peers.

- For this part, you will need 4 machines with all the code and dependencies installed.

#### Creating Torrent Files  Instructions

    The sender needs to  creates the .torrent file which will be used to send files to the peers.

    - CMD: py3createtorrent -t udp://tracker.opentrackr.org:1337/announce <path-to-file>

    Example:
    - py3createtorrent -t udp://tracker.opentrackr.org:1337/announce A_10kB
    
    This creates a torrent file (A_10kB.torrent) that is sent to the peers.

#### Seeder Running Instructions
- On first machine (Seeder), run the seeder code using the following command:
    ```
    - CMD: python seeder.py <path-to-torrent-file> <total-runs>
    Example:
    - python seeder.py A_10kB.torrent 333
    ```
#### Leecher Running Instructions
- Once the torrent files are copied and seeder is running, run the leecher using the following command:
    ```
    To run the peer (receiver):
    - CMD: python leecher.py <path-to-torrent-file> <total-runs> <file-size in Bytes>
    Example:
    - python leecher.py A_10kB.torrent 333 10240
    ```
    - File Sizes are as follows:
        -  10kB = 10240 Bytes
        - 100kB = 102400 Bytes
        - 1MB = 1048576 Bytes
        - 10MB = 10485760 Bytes

    - This will download the files from the seeder.
    - Run the leecher code on all the 3 machines to download the files from the seeder.
    - The leecher code will download the files and save them in the same folder where the leecher code is present.


## Analysing the Results
- For each client-server protocol, the results for Type A and Type B file transfer are separately printed in the terminal and also saved in respective .csv files.
- These results needs to be combined to get final mean and standard deviation for each protocol and each size of file.
    - For each size of file, two results are printed in the terminal. One for Type A file transfer and one for Type B file transfer. To combine these results, we can use following formula:
        ```
        Mean = (NA * MA + NB * MB) / (NA + NB)
        Standard Deviation = sqrt[{(NA-1)(SA^2) + (NB-1)(SB^2) + [NA*NB*(MA-MB)^2/(NA+NB1)]}/(NA+NB-1)]
        ```
        - Where NA and NB are the number of samples for Type A and Type B file transfer respectively.
        - MA and MB are the mean for Type A and Type B file transfer respectively.
        - SA and SB are the standard deviation for Type A and Type B file transfer respectively.
    - Can use following website to calculate the mean and standard deviation: https://www.statstodo.com/CombineMeansSDs.php
- For BitTorrent, the results are printed in the terminal and also saved in a .csv file.
    - We were unable to get results at senders end. We were able to get results at receivers end only. So, we have results for only one end. 
    - We used the results from three receivers to calculate the mean and standard deviation using the above formula and then multiplied the mean and standard deviation by 3 to get the final mean and standard deviation for BitTorrent.
    - Also we faced a lot of issues running the bitTorrent code, for one seeder and one leecher it works fine but for multiple leechers it was not working properly. We had to try multiple times to get the results.
