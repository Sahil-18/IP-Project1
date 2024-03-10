import libtorrent as lt
import sys
import time
import threading

# Function to create a torrent for a given file
def create_torrent(file_path, tracker_url):
    print(file_path)
    fs = lt.file_storage()
    lt.add_files(fs, file_path)
    
    t = lt.create_torrent(fs)
    t.add_tracker(tracker_url, 0)
    t.set_creator('libtorrent %s' % lt.version)
    t.set_comment("Test")
    lt.set_piece_hashes(t, ".")
    
    return t.generate()

# Function to seed a torrent
def seed_torrent(torrent_file, save_path, port):
    name = torrent_file.split(".")[0]
    ses = lt.session()
    ses.listen_on(port, port + 10)
    i = 0
    total_data_transfered = 0
    total_payload_transfered = 0
    
    h = ses.add_torrent({'ti': lt.torrent_info(torrent_file), 'save_path': save_path}) 
    while True:
        # ses = lt.session()
        # ses.listen_on(port, port + 10)
 
        h = ses.add_torrent({'ti': lt.torrent_info(torrent_file), 'save_path': save_path})
        print(name , " Seeding... ", i)
        s = h.status()

        while not s.is_seeding:
            s = h.status()
            total_data_transfered = s.total_upload
            total_payload_transfered = s.total_payload_upload
            state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

            print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
            sys.stdout.flush()
            time.sleep(1)
        ses.remove_torrent(h)
        ses.post_torrent_updates()
        print(f"Seeding {i} of {name} complete")
        i+=1
        print("Upload data : ", total_data_transfered, name)
        print("total payload : ", total_payload_transfered, name)
    

# Paths to the files you want to share
file_paths = ['A_10kB', 'A_100kB', 'A_1MB', 'A_10MB']
# file_paths = ['A_10kB']

# Tracker URL
# tracker_url = "tcp://tracker.openbittorrent.com:80/announce"
tracker_url = "udp://tracker.opentrackr.org:1337/announce"

# Ports for each torrent
ports = [6881, 6882, 6883, 6884]

# Generate and save .torrent files for each file
for i, file_path in enumerate(file_paths):
    torrent_data = create_torrent(file_path, tracker_url)
    with open(f"{file_path}.torrent", "wb") as f:
        f.write(lt.bencode(torrent_data))

# while True:
# seed_torrent("A_10kB.torrent", ".", 6881)

# Seed each torrent in a separate thread


for i, file_path in enumerate(file_paths):
    threading.Thread(target=seed_torrent, args=(f"{file_path}.torrent", '.', ports[i])).start()
