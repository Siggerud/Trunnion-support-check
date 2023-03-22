import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url):
        self._url = url
        self._soup = self._getSoup()


    def _getSoup(self):
        response = requests.get(self._url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        return soup

    def getSoup(self):
        return self._soup

    def find(self, tag, elementType, attributeSet=(None, None)):
        if attributeSet == (None, None):
            return tag.find(elementType)

        attribute, value = attributeSet
        if attribute == "class":
            return tag.find(elementType, _class=value)


    def findAll(self, tag, elementType, attributeSet=(None, None)):
        if attributeSet == (None, None):
            return tag.find_all(elementType)

        attribute, value = attributeSet
        if attribute == "class":
            return tag.find_all(elementType, class_=value)

