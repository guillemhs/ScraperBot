import parsers.parser_youporn
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup

def scraping_homepage(br, htmlscraper, parser, output):
    print "scraping homepage"
    reu = parser.get_video_box()
    ii = parser.get_title()
    print parser.split_title(str(ii[0]))
    url = "http://www.youporn.com" + htmlscraper.parse_href(reu[0])
    print url
    print parser.get_thumbnail(reu[0])
    paraVideo = parser.parse_video_id(url)
    print parser.create_video_iframe(paraVideo[0], paraVideo[1])
    videoPage = br.scrap_website(htmlscraper.parse_href(url))
    soup = BeautifulSoup(videoPage)


def scraping_categories(br, htmlscraper, parser, output):
    print "scraping categories"


br = common.startBrowser.BotBrowser()
homepage = br.scrap_website('http://www.youporn.com/')
htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
parser = parsers.parser_youporn.YoupornParser(homepage)

scraping_homepage(br, htmlscraper, parser, homepage)

print "Scraping finished"