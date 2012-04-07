import urllib2

from bs4 import BeautifulSoup, SoupStrainer

page = urllib2.urlopen("http://Www.google.com")
soup = BeautifulSoup(page)

links = SoupStrainer('a')


#print soup.prettify()

titleTag = soup.html.head.title

print titleTag.string

print len(soup('p'))

soup.findAll('<script>')

