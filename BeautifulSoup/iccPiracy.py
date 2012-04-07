import urllib2

from bs4 import BeautifulSoup

class iccPiracy():
    page = urllib2.urlopen("http://www.mitorestaurant.com/")
    soup = BeautifulSoup(page)

    #print soup.prettify()

    for i in soup.find_all("class"):
        print i
