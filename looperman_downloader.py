from bs4.element import SoupStrainer
from link2mp3 import get_mp3_link
from bs4 import BeautifulSoup
import requests
import sys
import re

LOOP_DETAIL_REGEX = ".*loops/detail/.*/.*"

class Looperman_Downloader:
    amount = 0
    url = ""
    soup = BeautifulSoup()
    links = []

    def __init__(self, url, amount):
        self.data = []
        self.url = url
        self.amount = amount
        self.download()

    def download(self):
        #while len(self.links) != self.amount:
        self.move_to_page()
        self.get_song_links_of_page()
        self.move_to_next_page()

    def get_song_links_of_page(self):
        for link in self.soup.findAll('a'):

            if len(self.links) == self.amount:
                break

            href = link.get('href')
            is_a_song = bool(re.match(LOOP_DETAIL_REGEX,href))
            if is_a_song and href not in self.links:
                self.links.append(href)

    def move_to_page(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, features="html.parser")

    def move_to_next_page(self):
        page_equald_idx = self.url.find("=") 
        page_number = ""
        number_idx = page_equald_idx + 1

        while self.url[number_idx].isdigit():
            page_number += self.url[number_idx]
            number_idx += 1

        # replace page number with next one
        self.url = re.sub("page=\d*", "page="+str(int(page_number)+1), self.url)
    
def main():
    url = sys.argv[1]
    amount = sys.argv[2]
    Looperman_Downloader(url, amount)

if __name__ == "__main__":
    main()