import re

from BeautifulSoup import BeautifulSoup

class YoupornParser():
    "A youporn simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup

    def get_video_td(self):
        results = []
        for tag in self.soup.findAll("li", { "class":"videoBox" }):
            results.append(tag)
        return results
