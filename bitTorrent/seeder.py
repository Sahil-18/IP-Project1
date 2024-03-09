# # Write a bittorrent seeder
# # The leecher is on different machine
# # The seeder is on different machine
# # Seeder needs to send multiple files to the leecher when requested
# # The leecher will request the file from the seeder


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
    ses = lt.session()
    ses.listen_on(port, port + 10)
    
    h = ses.add_torrent({'ti': lt.torrent_info(torrent_file), 'save_path': save_path}) 

    while True:
        s = h.status()
        state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

        print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
        sys.stdout.flush()

        time.sleep(1)

# Paths to the files you want to share
file_paths = ['A_10kB', 'A_100kB', 'A_1MB', 'A_10MB']

# Tracker URL
tracker_url = "udp://tracker.openbittorrent.com:80/announce"

# Ports for each torrent
ports = [6881, 6882, 6883, 6884]

# Generate and save .torrent files for each file
for i, file_path in enumerate(file_paths):
    torrent_data = create_torrent(file_path, tracker_url)
    with open(f"{file_path}.torrent", "wb") as f:
        f.write(lt.bencode(torrent_data))

# Seed each torrent in a separate thread


for i, file_path in enumerate(file_paths):
    threading.Thread(target=seed_torrent, args=(f"{file_path}.torrent", '.', ports[i])).start()
