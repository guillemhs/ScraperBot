import parsers.parser_youporn
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup

def scraping_homepage(br, htmlscraper, parser, output):
    print "scraping homepage"
    reu = parser.get_video_box()
    for i in range(len(reu)):
        try:
            print "---------------------" + str(i) + " from " + str(len(reu)) + "------------------------"
            title = htmlscraper.convert_hypen_into_space(parser.split_url(htmlscraper.parse_href(reu[i])))
            print "title: " + title
            title_as_categories = htmlscraper.convert_title_to_categories(str(title))
            print "title convert to categories: " + str(title_as_categories)
            url = "http://www.youporn.com" + htmlscraper.parse_href(reu[i])
            print "url: " + url
            print "url objects: " + htmlscraper.convert_hypen_into_space(parser.split_url(url))
            strIntoCategories = htmlscraper.convert_hypen_into_space(parser.split_url(url))
            print htmlscraper.convert_string_into_categories(strIntoCategories)
            print "thumbnail: " + parser.get_thumbnail(reu[i])
            paraVideo = parser.parse_video_id(url)
            print "iframe: " + parser.create_video_iframe(paraVideo[0], paraVideo[1])
            soup = BeautifulSoup(br.scrap_website(url))
            cat_and_tags = parser.get_tags_and_categories(soup)
            cats = BeautifulSoup(str(cat_and_tags[0]))
            print "categories: " + parser.extract_categories(htmlscraper.parse_all_href(cats))
            tags = BeautifulSoup(str(cat_and_tags[1]))
            print "tags: " + parser.extract_categories(htmlscraper.parse_all_href(tags))
            print "video duration: " + parser.get_duration(soup)
        except:
            pass

print "Youporn scraper bot is starting ..."
br = common.startBrowser.BotBrowser()
homepage = br.scrap_website('http://www.youporn.com/')
htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
parser = parsers.parser_youporn.YoupornParser(homepage)

scraping_homepage(br, htmlscraper, parser, homepage)

print "Scraping finished"