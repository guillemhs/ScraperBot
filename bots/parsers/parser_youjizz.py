from BeautifulSoup import BeautifulSoup
import re

class YouJizzParser():
    "A YouJizz simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup

    def getUrlsFromVideos(self, output):
        results = []
        print output
        for link in output.findAll('a'):
            try:
                href = link['href']
                print href
            except KeyError:
                pass
        return results

    def getUrlsFromCategories(self, output):
        global resultsForCategories
        resultsForCategories = []
        match = re.compile('(xvideos\.com\/c\/)([-a-zA-Z0-9_]+)')
        for link in self.soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    resultsForCategories.append(href)
            except KeyError:
                pass
        return resultsForCategories
