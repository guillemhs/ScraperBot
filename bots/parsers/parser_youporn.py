from BeautifulSoup import BeautifulSoup
import re

class YoupornParser():
    "A youporn simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup

    def get_video_box(self):
        results = []
        for tag in self.soup.findAll("li", { "class":"videoBox" }):
            results.append(tag)
        return results

    def get_title(self):
        results = []
        for tag in self.soup.findAll("h1"):
            results.append(tag)
        results.pop(0) #remove the tag <h1 class="title">Videos Being Watched Now</h1>
        return results

    def split_title(self, output):
        auxOutput = output.split('>')
        auxOutput = auxOutput[2].split('<')
        return auxOutput[0]

    def get_thumbnail(self, output):
        global auxThumbnail, thumbnailStruct
        auxThumbnail = []
        thumbnailStruct = []
        for tag in output.findAll('img'):
            auxThumbnail = tag
        thumbnailStruct = str(auxThumbnail).split('"')
        return thumbnailStruct[1]

    def get_tags_and_categories(self, output):
        global auxResults
        auxResults = []
        for tag in output.findAll("ul", { "class":"listCat" }):
            auxResults.append(tag)
        return auxResults

    def extract_categories(self, output):
        final_categories = []
        for i in output:
            aux = i
            if len(aux) > 2:
                final_categories.append(aux[len(aux) - 2])
        return final_categories

    def split_url(self, output):
        aux = output.split("/")
        return aux[len(aux) - 2]

    def parse_video_id(self, output):
        global auxOutput
        auxOutput = output.lstrip('http://www.youporn.com/watch').split('/')
        return auxOutput

    def get_duration(self, output):
        authordiv = output.findAll('h2', attrs={'class': 'duration'})
        print output
        print authordiv
        return str(authordiv)

    def getUrlsFromVideos(self, soup, htmlscraper):
        results = []
        match = re.compile('(?<=\/watch/)([a-zA-Z0-9_-])+')
        for link in soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    final_result = "http://www.youporn.com" + href
                    results.append(final_result)
            except KeyError:
                pass
        return results

    def getUrlsFromCategories(self, soup, htmlscraper):
        results = []
        match = re.compile('(?<=\/category/)([a-zA-Z0-9_-])+')
        for link in soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    final_result = "http://www.youporn.com" + href
                    results.append(final_result)
            except KeyError:
                pass
        return results

    def create_video_iframe(self, in1, in2):
        return "<iframe src=\"http://www.youporn.com/embed/" + in1 + "/" + in2 + "/\" frameborder=\'0\' height=\'485\' width=\'615\' scrolling=\'no\' name=\'yp_embed_video\'></iframe>"