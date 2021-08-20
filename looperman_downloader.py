from bs4 import BeautifulSoup
import requests
import sys
import re
from session_utils import login
from loop import Loop

LOOP_DETAIL_REGEX = ".*loops/detail/.*/.*"
LOOP_FORMAT = ""
SETTINGS_FORMAT = "KEY_FROMBPM_TOBPM_CAT_GENRE"

CATEGORY = "gid"
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

USERNAME = ""
PASSWORD = ""


class Looperman_Downloader:
    url = ""
    soup = BeautifulSoup()
    loops = []
    logged_in = False

    def __init__(self, url, amount):
        self.data = []
        self.url = url
        self.amount = amount
        self.download()

    def download(self):
        self.login()
        self.get_fitler_settings()

        #while len(self.loops) < self.amount:
        self.get_loops()
            #self.move_to_next_page()

    """
    Gets the filter settings
    """

    def get_fitler_settings(self):
        SETTINGS[CATEGORY] = self.find_filter_selection(CATEGORY)
        SETTINGS[GENRE] = self.find_filter_selection(GENRE)
        SETTINGS[KEY] = self.find_filter_selection(KEY)
        SETTINGS[FROM_BPM] = self.find_filter_input(FROM_BPM)
        SETTINGS[TO_BPM] = self.find_filter_input(TO_BPM)

    """
    Gets the loop download links and saves their information
    """

    def get_loops(self):
        idx = 0
        tags = self.soup.find_all("div", attrs={"class": "tag-wrapper"})
        titles = self.soup.find_all("a", attrs={"class": "player-title"})

        for player_wrapper in self.soup.find_all("div", attrs={"class": "player-wrapper"}):

            if len(self.loops) == self.amount:
                break

            title = titles[idx].get_text()
            bpm = tags[idx].find("a").getText()

            if self.logged_in:
                link = self.get_wav_link(player_wrapper)
            else:
                link = self.get_mp3_link(player_wrapper)

            print(link)

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

    def get_wav_link(self, player_wrapper):
        return player_wrapper.find("a", class_="player-big-btn btn-download trkd")["href"]

    """
    Gets all mp3 links from player wrappers of one search page
    """

    def get_mp3_link(self, player_wrapper):
        return player_wrapper["rel"]

    """
    Increases the page number inside the url link by one
    and moves to that page 
    """

    def move_to_next_page(self):
        page_equald_idx = self.url.find("=")
        page_number = ""
        number_idx = page_equald_idx + 1

        while self.url[number_idx].isdigit():
            page_number += self.url[number_idx]
            number_idx += 1

        # replace page number with next one
        self.url = re.sub("page=\d*", "page=" +
                          str(int(page_number)+1), self.url)

        self.move_to_url()

    """
    Tries a log in attempt to get Wav downloads.
    Otherwise only mp3 files are available
    """

    def login(self):
        self.session = requests.Session()
        login(USERNAME, PASSWORD, self.session)

        self.move_to_url()

        logout_href = self.soup.find(
            "div", attrs={"class": "nav-account"}).find("a")["href"]
        self.logged_in = "logout" in logout_href

    """
    Moves to the url by requesting it and downloading the html
    """

    def move_to_url(self):
        r = self.session.get(self.url)
        self.soup = BeautifulSoup(r.text, features="html.parser")

    """
    Returns selected attribute of id field in filter 
    """

    def find_filter_selection(self, id):
        return self.soup.find("select", attrs={"name": id}).find("option", attrs={"selected": "selected"}).get_text()

    def find_filter_input(self, id):
        return self.soup.find("input", attrs={"id": id})["value"]


def main():
    url = sys.argv[1]
    amount = sys.argv[2]
    Looperman_Downloader(url, int(amount))


if __name__ == "__main__":
    main()
