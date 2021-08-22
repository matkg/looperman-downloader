import requests
import shutil
import os
import errno

def download_file(session, url, filename, file_end):
    if os.path.isfile(filename):
        print(f"File already exists! Skipping: {filename}")
        return

    filename = filename+file_end

    create_dirs(filename)
    print(f"Download file {filename}")

    with session.get(url, stream=True) as r:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return filename

def create_dirs(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise