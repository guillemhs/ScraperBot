import parsers.parser_youporn
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup

def scraping_homepage(br, htmlscraper, parser, output):
    print "scraping homepage"
    reu = parser.get_video_box()
    for i in range(len(reu)):
        ii = parser.get_title()
        print parser.split_title(str(ii[0]))
        url = "http://www.youporn.com" + htmlscraper.parse_href(reu[i])
        print url
        print parser.get_thumbnail(reu[i])
        paraVideo = parser.parse_video_id(url)
        print parser.create_video_iframe(paraVideo[0], paraVideo[1])
        try:
            soup = BeautifulSoup(br.scrap_website(url))
            cat_and_tags = parser.get_tags_and_categories(soup)
            #print cat_and_tags[0]
            cats = BeautifulSoup(str(cat_and_tags[0]))
            print htmlscraper.parse_all_href(cats)
            #print cat_and_tags[1]
            tags = BeautifulSoup(str(cat_and_tags[1]))
            print htmlscraper.parse_all_href(tags)
        except:
            pass

def scraping_categories(br, htmlscraper, parser, output):
    print "scraping categories"


br = common.startBrowser.BotBrowser()
homepage = br.scrap_website('http://www.youporn.com/')
htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
parser = parsers.parser_youporn.YoupornParser(homepage)

scraping_homepage(br, htmlscraper, parser, homepage)

print "Scraping finished"