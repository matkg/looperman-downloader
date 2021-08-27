# looperman-downloader

Downloads a specific amount of loops from looperman.com to a designated location. Credentials must be specified inside credentials.py 
in order to be able to download wav files. Otherwise only the mp3 previews will get downloaded.

## Installation
Install Python > v3.8.5
```bash
pip install -r requirements.txt
``` 

## Usage

⚠️ **Be aware that your account or ip address could get blocked if you make excessive use of this script!**
<br><br>

The script saves loops under the following structure
```bash
<download destination>/Looperman_Loops/<genre>/<category>/<key>_<bpm>_bpm_<title>.wav
``` 

Usage
```bash
python looperman_downloader.py <looperman search url> <amount of loops to download> <download destination>
```

Example
```bash
python looperman_downloader.py "https://www.looperman.com/loops?page=1&cid=33&gid=54&mkey=am&order=date&dir=d" 100 "D:\Music\Loops"
```

