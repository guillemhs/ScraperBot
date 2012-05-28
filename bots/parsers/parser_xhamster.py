from BeautifulSoup import BeautifulSoup
import re

class xHamsterParser():
    "A xHamster simple parser class."

    def __init__(self, output):
        soup = BeautifulSoup(output)
        self.soup = soup

    def getUrlsFromVideos(self, output):
        auxOutput = []
        for link in output.findAll("a", { "class":"hRotator" }):
            try:
                href = link['href']
                href = "http://www.xhamster.com/" + href
                auxOutput.append(href)
            except KeyError:
                pass
        return auxOutput

    def getUrlsFromCategories(self, output):
        global resultsForCategories
        resultsForCategories = []
        match = re.compile('(xhamster\.com\/channels\/)([-a-zA-Z0-9_]+)')
        for link in self.soup.findAll('a'):
            try:
                href = link['href']
                if re.search(match, href):
                    resultsForCategories.append(href)
            except KeyError:
                pass
        return resultsForCategories

    def split_url(self, output):
        aux = output.split("/")
        preprod = str(aux[6])
        var = preprod.split('.')
        return str(var[0])

    def get_thumbnail(self, output):
        global auxThumbnail, thumbnailStruct
        auxThumbnail = []
        thumbnailStruct = []
        for tag in output.findAll("a", { "class":"hRotator" }):
            td = tag
        newSoup = BeautifulSoup(str(td))
        for image in newSoup.findAll("img"):
            return str(image['src'])

    def parse_video_id(self, output):
        aux = output.split("/")
        return str(aux[5])

    def create_video_iframe(self, output):
        return "<iframe width=\"510\" height=\"400\" src=\"http://xhamster.com/xembed.php?video=" + output + "\" frameborder=\"0\" scrolling=\"no\"></iframe>"

    def get_duration(self, incomingSoup):
        auxThumbnail = []
        for tag in incomingSoup.findAll("table", { "class":"stats_table" }):
            td = tag
        newSoup = BeautifulSoup(str(td))
        for image in newSoup.findAll("td"):
            auxThumbnail.append(image)
        strToSplit = str(auxThumbnail[5])
        aux = strToSplit.split("<td>")
        aux2 = str(aux[1])
        aux3 = aux2.split("</td>")
        return aux3[0]

    def prepare_duration_for_snippets(self, duration):
        #format T30M00S
        min = duration.split('m')
        minute = str(min[0]).strip()
        if len(minute) == 1:
            newMinute = "0" + str(minute)
        else:
            newMinute = str(minute)
        sec = min[1].split('s')
        second = str(sec[0]).strip()
        if len(second) == 1:
            newSecond = "0" + str(second)
        else:
            newSecond = str(second)
        newDuration = "T" + newMinute + "M" + newSecond + "S"
        print newDuration
        return newDuration