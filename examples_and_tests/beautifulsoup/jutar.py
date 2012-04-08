from urllib import urlopen

from bs4 import BeautifulSoup # To get everything
Soup = BeautifulSoup



url = "http://www.jutarnji.hr"
html_doc = urlopen( url ).read()
soup = Soup( html_doc )
soup.prettify()
soup.find_all( "a", {"class":"black"} )