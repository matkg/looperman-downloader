from bs4 import BeautifulSoup
import requests
import sys
import re
from session_utils import login
from loop import Loop
from file_utils import download_file
from os import path

CATEGORY = "cid"
GENRE = "gid"
KEY = "mkey"
FROM_BPM = "ftempo"
TO_BPM = "ttempo"

SETTINGS = {
    CATEGORY: "",  # Category ID
    GENRE: "",  # Genre ID
    KEY: "",  # Key
    FROM_BPM: "",  # From tempo
    TO_BPM: ""  # To tempo
}

class LoopermanDownloader:
    url = ""
    soup = BeautifulSoup()
    loops = []
    logged_in = False

    def __init__(self, url, amount, location):
        self.data = []
        self.url = url
        self.amount = int(amount)
        self.location = path.join(location, "")

    """
    Performs the download of the desired amount of loops
    """
    def download(self):
        self.__login()
        self.__get_fitler_settings()

        remaining = self.amount

        while len(self.loops) < remaining:
            self.__get_loops()
            self.__download_files()

            remaining -= len(self.loops)
            self.loops = []
            self.__move_to_next_page()

    """
    Gets the filter settings
    """

    def __get_fitler_settings(self):
        SETTINGS[CATEGORY] = self.__find_filter_selection(CATEGORY)
        SETTINGS[GENRE] = self.__find_filter_selection(GENRE)
        SETTINGS[KEY] = self.__find_filter_selection(KEY)
        SETTINGS[FROM_BPM] = self.__find_filter_input(FROM_BPM)
        SETTINGS[TO_BPM] = self.__find_filter_input(TO_BPM)

    """
    Gets the loop download links and saves their information
    """

    def __get_loops(self):
        idx = 0
        tags = self.soup.find_all("div", attrs={"class": "tag-wrapper"})
        titles = self.soup.find_all("a", attrs={"class": "player-title"})
        wav_links = self.soup.select('a[href*=".com/getfiles"]')

        for player_wrapper in self.soup.find_all("div", attrs={"class": "player-wrapper"}):

            if len(self.loops) == self.amount:
                break

            title = titles[idx].get_text()
            bpm = tags[idx].find("a").getText()

            if self.logged_in:
                link = wav_links[idx]["href"]
            else:
                link = self.__get_mp3_link(player_wrapper)

            loop = Loop(
                genr=SETTINGS[GENRE],
                key=SETTINGS[KEY],
                cat=SETTINGS[CATEGORY],
                title=title,
                dl_link=link,
                bpm=bpm
            )

            self.loops.append(loop)
            idx += 1

    """
    Downloads all loop files
    """
    def __download_files(self):
        for loop in self.loops:
            file_end = ".wav" if self.logged_in else ".mp3"
            filename = f"{self.location}Looperman Loops/{loop.genre}/{loop.category}/{loop.key} {loop.bpm} {loop.title}"
            filename = filename.replace(" ", "_")
            download_file(self.session, loop.download_link, filename, file_end)


    """
    Gets all mp3 links from player wrappers of one search page
    """

    def __get_mp3_link(self, player_wrapper):
        return player_wrapper["rel"]

    """
    Increases the page number inside the url link by one
    and moves to that page 
    """

    def __move_to_next_page(self):
        page_equald_idx = self.url.find("=")
        page_number = ""
        number_idx = page_equald_idx + 1

        while self.url[number_idx].isdigit():
            page_number += self.url[number_idx]
            number_idx += 1

        # replace page number with next one
        self.url = re.sub("page=\d*", "page=" +
                          str(int(page_number)+1), self.url)

        self.__move_to_url()

    """
    Tries a log in attempt to get Wav downloads.
    Otherwise only mp3 files are available
    """

    def __login(self):
        self.session = requests.Session()
        login(self.session)

        self.__move_to_url()

        nav_account = self.soup.find("div", attrs={"class": "nav-account"})
        for link in nav_account.find_all("a"):
            url = link["href"]
            if "profile/" in url:
                self.logged_in = True
                print(f"Logged in as:\n{url}")
        
        if not self.logged_in:
            print("Logging in failed, proceeding to download mp3 files")

    """
    Moves to the url by requesting it and downloading the html
    """

    def __move_to_url(self):
        r = self.session.get(self.url)
        self.soup = BeautifulSoup(r.text, features="html.parser")
        print(f"Moved to: {self.url}")

    """
    Returns selected attribute of id field in filter from dropdown
    """

    def __find_filter_selection(self, id):
        return self.soup.find("select", attrs={"name": id}).find("option", attrs={"selected": "selected"}).get_text()

    """
    Returns text input from filter field
    """
    def __find_filter_input(self, id):
        return self.soup.find("input", attrs={"id": id})["value"]

"""
Usage: .\looperman_downloader.py [URL] [AMOUNT] [LOCATION]
"""
def main():
    url = sys.argv[1]
    amount = "10" if len (sys.argv) < 3 else sys.argv[2]
    location = "./" if len(sys.argv) < 4 else sys.argv[3]
    LoopermanDownloader(url, amount, location).download()


if __name__ == "__main__":
    main()
