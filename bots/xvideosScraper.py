import parsers.parser_xvideos
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup

def scraping_homepage(br, htmlscraper, parser, output):
    videoduration = parser.get_video_td()
    for i in range(len(videoduration)):
        try:
            print "---------------------" + str(i) + " from " + str(len(videoduration)) + "------------------------"
            title = parser.get_title_on_homepage(videoduration[i])
            title = parser.split_title(str(title))
            print "title: " + title
            title_as_categories = htmlscraper.convert_title_to_categories(title)
            print "title convert to categories: " + title_as_categories
            url = htmlscraper.parse_href(videoduration[i])
            print "url: " + url
            videoduration1 = parser.get_video_duration(videoduration[i])
            thumbnail = parser.get_thumbnail(videoduration[i])
            print "thumbnail: " + thumbnail
            duration = parser.split_video_duration(str(videoduration1))
            print "duration: " + duration
            video_id = parser.parse_video_id(videoduration[i])
            iframe_object = parser.create_video_iframe(str(video_id[0]))
            print "iframe: " + iframe_object
            videoPage = br.scrap_website(htmlscraper.parse_href(videoduration[i]))
            soup = BeautifulSoup(videoPage)
            print "tags: " + parser.parse_tags(htmlscraper.parse_all_href(soup))

        except:
            pass

def scraping_categories(br, htmlscraper, parser, output):
    parser = parsers.parser_xvideos.XvideosParser(output)
    categories = parser.parse_categories(output)
    for j in categories:
        print "Parsing " + j + " ... "
        xvideoscategory = br.scrap_website(j)
        soup = BeautifulSoup(xvideoscategory)
        videoduration = parser.get_video_td_from_categories(soup)
        for i in range(len(videoduration)):
            try:
                print "---------------------" + str(i) + " from " + str(len(videoduration)) + "------------------------"
                title = parser.get_title_on_homepage(videoduration[i])
                title = parser.split_title(str(title))
                print "title: " + title
                title_as_categories = htmlscraper.convert_title_to_categories(title)
                print "title convert to categories: " + title_as_categories
                url = htmlscraper.parse_href(videoduration[i])
                print "url: " + url
                videoduration1 = parser.get_video_duration_on_categories(videoduration[i])
                thumbnail = parser.get_thumbnail(videoduration[i])
                print "thumbnail: " + thumbnail
                duration = parser.split_video_duration_on_categories(str(videoduration1))
                print "duration: " + duration
                video_id = parser.parse_video_id(videoduration[i])
                iframe_object = parser.create_video_iframe(str(video_id[0]))
                print "iframe: " + iframe_object
                videoPage = br.scrap_website(htmlscraper.parse_href(videoduration[i]))
                soup = BeautifulSoup(videoPage)
                print "tags: " + parser.parse_tags(htmlscraper.parse_all_href(soup))

            except:
                pass


print "xVideos scraper bot is starting ..."
br = common.startBrowser.BotBrowser()
xvideoshomepage = br.scrap_website('http://www.xvideos.com/')
htmlscraper = common.html_tag_parser.HtmlTagParser(xvideoshomepage)
parser = parsers.parser_xvideos.XvideosParser(xvideoshomepage)

scraping_homepage(br, htmlscraper, parser, xvideoshomepage)
scraping_categories(br, htmlscraper, parser, xvideoshomepage)

print "Scraping finished"