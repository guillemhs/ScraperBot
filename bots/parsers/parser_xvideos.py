import re

from BeautifulSoup import BeautifulSoup

class XvideosParser():
    "A xvideos simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup

    def get_keywords(self):
        return self.soup.findAll(attrs={"name":"KEYWORDS"})

    def get_title_on_homepage(self, output):
        for tag in output.findAll('span'):
            return tag

    def get_title_on_videopage(self):
        results = []
        for tag in self.soup.findAll('strong'):
            results.append(tag)
        return results[4]

    def get_video_td(self):
        results = []
        for tag in self.soup.findAll("td", { "width":"183" }):
            results.append(tag)
        return results

    def get_video_duration(self, output):
        for tag in output.findAll('b'):
            return tag

    def parse_videos(self):
        results = []
        match = re.compile('(xvideos\.com\/video)([-a-zA-Z0-9_]+)')
        for link in self.soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    results.append(href)
            except KeyError:
                pass
        return results

    def parse_categories(self, output):
        results = []
        match = re.compile('(xvideos\.com\/c\/)([-a-zA-Z0-9_]+)')
        for link in self.soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    results.append(href)
            except KeyError:
                pass
        return results

    def parse_video_id(self, output):
        match = re.compile('(?<=xvideos\.com\/video)([-a-zA-Z0-9_]+)')
        for link in output.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    auxOutput = href.lstrip('http://www.xvideos.com/video').split('/')
            except KeyError:
                pass
        return auxOutput

    def create_video_iframe(self, output):
        return "<iframe src=\"http://flashservice.xvideos.com/embedframe/" + output + "\" frameborder=0 width=510 height=400 scrolling=no></iframe>"

