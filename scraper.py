import requests
from bs4 import BeautifulSoup

class Scraper:
    # class to quickly make a BeautifulSoup object
    def __init__(self, url):
        self._url = url

    # gets soup object
    def getSoup(self):
        response = requests.get(self._url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        return soup


