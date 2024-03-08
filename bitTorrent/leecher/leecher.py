import libtorrent as lt
import sys
import time

# Create a leecher to download the file

ses = lt.session()
ses.listen_on(6881, 6891)
# Add a torrent
e = lt.bdecode(open("../mytorrent.torrent", 'rb').read())
info = lt.torrent_info(e)
h = ses.add_torrent({'ti': info, 'save_path': '.'})
s = h.status()
	
# Fetch the file
while not s.is_seeding:
    s = h.status()

    state_str = ['queued', 'checking', 'downloading metadata', \
      'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

    print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
    sys.stdout.flush()

    time.sleep(1)

# from torrentp import TorrentDownloader
# torrent_file = TorrentDownloader("../mytorrent.torrent", '.')
# torrent_file.start_download()
# print("downloading")
    

