from bs4 import BeautifulSoup # To get everything
import urllib2

page = urllib2.urlopen( "http://Www.google.com" )
soup = BeautifulSoup( page )


print soup.prettify()
