import urllib2, re

from bs4 import BeautifulSoup

page = urllib2.urlopen( "http://www.givegoodweb.com/examples/ogm-samples.html" )
soup = BeautifulSoup( page )
fontStart = re.compile( r'<font[a-zA-Z-",0-9= ]*>?' )
fontEnd = re.compile( r'</font>' )
titleSearch = re.compile( r'title=' )
getTitle = re.compile( r'<title>(.*)</title>', re.DOTALL | re.MULTILINE )
emailSearch = re.compile( r'mailto' )

def removeNL( x ):
    """cleans a string of new lines and spaces"""
    s = x.split( '\n' )
    s = [x.strip() for x in s]
    x = " ".join( s )
    return x.lstrip()

ul_tags = {}

for ul in soup.html.body.findAll( 'ul' ):
    links = []
    x = ul.findPrevious( 'font', color = "#3C378C" ).renderContents()
    if '\n' in x:
        x = removeNL( x )
    for li in ul.findAll( 'li' ):
        line = []
        for a in li.findAll( 'a' ):
            c = removeNL( str( a.contents[0] ) )
            c = fontStart.sub( '', c )
            c = fontEnd.sub( '', c )
            href = str( a.get( 'href' ) )
            if href[-3:].lower() == 'pdf':
                type = 'pdf'
                title = "PDF sample"
            elif emailSearch.search( href ):
                title = 'email'
            else:
                type = 'html'
                try:
                    f = urllib2.urlopen( href )
                    # reading in 2000 characters should to it
                    t = getTitle.search( f.read( 2000 ) )
                    if t :
                        title = t.group( 1 )
                        title = removeNL( title )
                    else : title = "open link"
                except urllib2.HTTPError, e:
                    title = 404
                f.close()
            if title != 404:
                line.append( ( c, href.lstrip( '/' ), type, title ) )
        links.append( line )
    ul_tags[x] = links

page.close()

f = open( 'samples.csv', 'w' )

for i in ul_tags.iterkeys():
    for x in ul_tags[i]:
        for t in x:
            f.write( '%s, %s, %s, %s, %s \n' % ( i, t[0], t[1], t[2], t[3] ) )

f.close()



