import libtorrent as lt
import sys
import timeit
from statistics import mean, stdev
import os
    

def download_torrent(file_path, torrent_file,num_requests, file_size):
    ses = lt.session()
    ses.listen_on(7072, 7082)
    RTT= []
    sizes = []
    thptvalues = []
    total_data_transfered = 0
    total_payload = 0

    for i in range(num_requests):
        print("Requesting ", i + 1)
        if os.path.exists(file_path):
            os.remove(file_path)
        # Add a torrent
        start = timeit.default_timer()
        total_data_transfered = 0
        total_payload = 0
        e = lt.bdecode(open(torrent_file , 'rb').read())
        info = lt.torrent_info(e)
        h = ses.add_torrent({'ti': info, 'save_path': '.'})
        s = h.status()
        # Fetch the file
        while not s.is_seeding:
            s = h.status()
            total_data_transfered = s.total_download
            total_payload = s.total_payload_download
            #state_str = ['queued', 'checking', 'downloading metadata',
                         #'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

            #print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                  #(s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
            sys.stdout.flush()

        end = timeit.default_timer()
        #total_payload = s.total_payload_download
        total_data_transfered = s.total_download
        total_payload = s.total_payload_download
        print("Total Data Transfered : ", total_data_transfered)
        print("Total Payload : ", total_payload)
        print("Total Done : ", s.total_done)
        RTT.append(end-start)
        sizes.append(total_data_transfered/file_size)
        thptvalues.append(file_size*0.008/(end-start))
        print("Completed ", i + 1, " request")
    ses.remove_torrent(h)

        # Create a csv file to store RTT, throughput and total data transfered with name as filename_results.csv
    with open(file_path + "_results.csv", 'w') as file:
        file.write("RTT,Throughput,TotalDataTransfered\n")
        for i in range(num_requests):
            file.write(str(RTT[i]) + "," + str(thptvalues[i]) + "," + str(sizes[i]) + "\n")

    # Calculate average RTT, throughput and total data transfered also standard Deviation
    # Also ensure that standard deviation is not calculated for 1 iteration
    # Save this in dictionary and return
    results = {}
    results["RTT"] = mean(RTT)
    results["Throughput"] = mean(thptvalues)
    results["TotalDataTransfered"] = mean(sizes)
    if num_requests > 1:
        results["Throughput_Std_Dev"] = stdev(thptvalues)
    else:
        results["Throughput_Std_Dev"] = 0
    return results

torrent_files = ['./A_10kB.torrent', './A_100kB.torrent', './A_1MB.torrent', './A_10MB.torrent']
file_paths = ['A_10kB', 'A_100kB', 'A_1MB', 'A_10MB']

result_A_10kB = download_torrent(file_paths[0], torrent_files[0], 10, 10240)
result_A_100kB = download_torrent(file_paths[1], torrent_files[1], 10, 102400)
result_A_1MB = download_torrent(file_paths[2], torrent_files[2], 10,1048576)
result_A_10MB = download_torrent(file_paths[3], torrent_files[3], 1, 10485760)

print("\nResults for A_10KB file")
print(result_A_10kB)

print("\nResults for A_100KB file")
print(result_A_100kB)

print("\nResults for A_1MB file")
print(result_A_1MB)

print("\nResults for A_10MB file")
print(result_A_10MB)
