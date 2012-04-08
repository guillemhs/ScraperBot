import urllib2
import re

from bs4 import BeautifulSoup

# find ".html" or ".pdf" in a string
match = re.compile('\.(com)')

response = urllib2.urlopen("http://Www.mitorestaurant.com")
page = BeautifulSoup(response)

# check links
for link in page.findAll('a'):
    try:
        href = link['href']
        if re.search(match, href):
            print href
    except KeyError:
        pass