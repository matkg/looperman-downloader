import shutil
import os
import errno
from time import sleep
import requests

def download_file(session, url, filename, file_end):
    filename = filename+file_end
    
    if os.path.isfile(filename):
        print(f"File already exists! Skipping: {filename}")
        return

    create_dirs(filename)
    print(f"Download file {filename}")

    with session.get(url, stream=True) as r:
        if r.status_code is not requests.codes.ok:
            print(r.json())
        
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    sleep(5) # necessary because of download limit

def create_dirs(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise