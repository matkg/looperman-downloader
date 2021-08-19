from bs4 import BeautifulSoup
import requests

"""
transforms looperman link in mp3 link example:
https://www.looperman.com/loops/detail/209709/nick-mira-x-foreigngotem-type-melody-150bpm-hip-hop-electric-guitar-loop to
https://www.looperman.com/media/loops/3280803/looperman-l-3280803-0209709-nick-mira-x-foreigngotem-type-melody.mp3
"""
def get_mp3_link(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="html.parser")

    r = soup.find_all("div", class_="player-wrapper")[0]
    r = str(r).split("\n")[0]

    url = r.split("rel")[1].replace('=', "").replace('"', "").replace(" >", "")

    return url