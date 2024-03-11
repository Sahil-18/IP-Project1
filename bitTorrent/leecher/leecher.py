import libtorrent as lt
import time
import sys
import os
import timeit
from statistics import mean, stdev

torr_file = sys.argv[1]
runs = int(sys.argv[2])
file_size = int(sys.argv[3])
file_path = torr_file.split(".")[0]
flag = False
files_recieved = 0
RTT= []
sizes = []
thptvalues = []
results = {}
total_data_transfered = 0
total_payload = 0
print("\n Waiting connect.")
while 1:
	ses = lt.session()
	ses.listen_on(6881, 6891)
	start = timeit.default_timer()
	info = lt.torrent_info(torr_file)
	h = ses.add_torrent({'ti': info, 'save_path': '.'})
	s = h.status()
	while (not s.is_seeding):
		s = h.status()
		print("progress", s.progress)
		if(s.progress != 0.0 and flag):
			print("\Getting the file")
			end = timeit.default_timer()
            #total_payload = s.total_payload_download\
			total_data_transfered = s.total_download
			total_payload = s.total_payload_download
			RTT.append(end-start)
			sizes.append(total_data_transfered/file_size)
			thptvalues.append(file_size*0.008/(end-start))
			flag = True
		if(s.progress == 1.0):
			files_recieved += 1
			print("\Received file ")
			end = timeit.default_timer()
            #total_payload = s.total_payload_download\
			total_data_transfered = s.total_download
			total_payload = s.total_payload_download
			RTT.append(end-start)
			sizes.append(total_data_transfered/file_size)
			thptvalues.append(file_size*0.008/(end-start))
			flag = False
			if(files_recieved == runs):
				print("\n Done")
				with open(file_path + "_results.csv", 'w') as file:
					file.write("RTT,Throughput,TotalDataTransfered\n")
					for i in range(runs):
						file.write(str(RTT[i]) + "," + str(thptvalues[i]) + "," + str(sizes[i]) + "\n")

				# Calculate average RTT, throughput and total data transfered also standard Deviation
				# Also ensure that standard deviation is not calculated for 1 iteration
				# Save this in dictionary and return
				results = {}
				results["RTT"] = mean(RTT)
				results["Throughput"] = mean(thptvalues)
				results["TotalDataTransfered"] = mean(sizes)
				if runs > 1:
					results["Throughput_Std_Dev"] = stdev(thptvalues)
				else:
					results["Throughput_Std_Dev"] = 0
				print(results)   
				exit()
			os.remove(torr_file.split(".")[0])

		sys.stdout.flush()
		time.sleep(1)