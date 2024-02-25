import libtorrent as lt
import time
import os
from dotenv import load_dotenv
load_dotenv()

def createTorrent(save_path):
    fs = lt.file_storage()
    # add the file stored at the path ../../dataFiles/computer1SendFiles/A_10kB
    A_file_path = os.getenv("A_FILES_LOCATION") + "A_10kB"
    fs.add_file(fs, A_file_path)
    t = lt.create_torrent(fs)
    t.add_tracker("udp://tracker.openbittorrent.com:80")
    t.set_piece_length(16 * 1024)

    torrent_path = save_path + ".torrent"
    with open(torrent_path, "wb") as f:
        f.write(lt.bencode(t.generate()))
    return torrent_path


def seedTorrent(save_path):
    torrent_path = createTorrent(save_path)
    ses = lt.session()

    info = lt.torrent_info(torrent_path)
    h = ses.add_torrent({"ti": info, "save_path": save_path})

    print("starting", h.name())

    # SEND FILE

    while not h.is_seed():
        s = h.status()
        print(s)
        time.sleep(1)

    print(h.name(), "complete")

if __name__ == "__main__":
    save_path = "/"
    seedTorrent(save_path)



