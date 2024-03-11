import libtorrent as lt
import sys
import time

torr_file = sys.argv[1]

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
    

seed_torrent(torr_file, ".", 6881)
