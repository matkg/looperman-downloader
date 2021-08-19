from bs4.element import SoupStrainer
from link2mp3 import get_mp3_link
from bs4 import BeautifulSoup
import requests
import sys

class Looperman_Downloader:
    amount = 0
    url = ""
    soup = BeautifulSoup()
    links = []

    def __init__(self, url, amount):
        self.data = []
        self.url = url
        self.amount = amount

    def download(self):
        self.move_to_page()
        self.get_song_links_of_page()

    def get_song_links_of_page(self):
        for link in self.soup.findAll('a'):
            href = link.get('href')
            if "loops/detail/" in href and href not in self.links:
                self.links.append(href)
        
        print(self.links)

    def move_to_page(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, features="html.parser")

def main():
    url = sys.argv[1]
    amount = sys.argv[2]
    Looperman_Downloader(url, amount)

if __name__ == "__main__":
    main()