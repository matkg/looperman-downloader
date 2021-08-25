import shutil
import os
import errno
from time import sleep
import requests
import magic

LIMIT_REACHED = "Sorry, due to high demand, download limits are in place and you have reached the limit.<br> Try again in 24 hours."
ITEM_LIMIT = "Sorry, download limit reached for this item. Try another file or try again in 24 hours."

def download_file(session, url, filename):
    
    if os.path.isfile(filename):
        print(f"File already exists! Skipping: {filename}")
        return False

    create_dirs(filename)
    print(f"Download file {filename}")

    with session.get(url, stream=True) as r:

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        sleep(7)

        filetype = magic.from_file(filename)

        if filetype == "gzip compressed data, from Unix":
            if r.text == LIMIT_REACHED:
                print("Download limit reached! Abort Downloading")
                exit()

            print("Soft limit reached! Sleeping 60 seconds")

            os.remove(filename)
            sleep(54)
            download_file(session, url, filename[:-4])

        elif "WAV" in filetype:
            return True

def create_dirs(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise