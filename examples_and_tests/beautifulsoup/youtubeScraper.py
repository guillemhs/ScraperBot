import urllib2

from bs4 import BeautifulSoup

class youtubeScraper():
    page = urllib2.urlopen("http://www.youtube.com/")
    soup = BeautifulSoup(page)

    #print soup.prettify()

    for i in soup.find_all("button"):
        print i
