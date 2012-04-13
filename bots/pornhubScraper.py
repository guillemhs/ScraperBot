import parsers.parser_youporn
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup

def scraping_homepage(br, htmlscraper, parser, output):
    print "scraping homepage"

def scraping_categories(br, htmlscraper, parser, output):
    print "scraping categories"


br = common.startBrowser.BotBrowser()
homepage = br.scrap_website('http://www.pornhub.com/')
htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
parser = parsers.parser_youporn.YoupornParser(homepage)