import sgmllib
import re

from BeautifulSoup import BeautifulSoup

class XvideosParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."

        for name, value in attributes:
            if name == "href":
                self.hyperlinks.append(value)

    def get_hyperlinks(self):
        "Return the list of hyperlinks."

        return self.hyperlinks

    def parse_href(self, output):
        results = []
        soup = BeautifulSoup(output)
        for tag in soup.findAll('a', href=True):
            results.append(tag['href'])
        return results

    def parse_xvideos_videos(self, output):
        results = []
        match = re.compile('(xvideos\.com\/video)([-a-zA-Z0-9_]+)')
        soup = BeautifulSoup(output)
        for link in soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    results.append(href)
            except KeyError:
                pass
        return results

    def parse_xvideos_categories(self, output):
        results = []
        match = re.compile('(xvideos\.com\/c\/)([-a-zA-Z0-9_]+)')
        soup = BeautifulSoup(output)
        for link in soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    results.append(href)
            except KeyError:
                pass
        return results

    def parse_xvideos_video_id(self, output):
        results = []
        match = re.compile('(?<=xvideos\.com\/video)([-a-zA-Z0-9_]+)')
        soup = BeautifulSoup(output)
        for link in soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    auxOutput = href.lstrip('http://www.xvideos.com/video').split('/')
                    results.append(auxOutput[0])
            except KeyError:
                pass
        return results

