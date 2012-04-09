import parsers.parser_xvideos
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup

def scraping_homepage(br, htmlscraper, parser, output):
    videoduration = parser.get_video_td()
    for i in range(len(videoduration)):
        try:
            print "---------------------" + str(i) + " from " + str(len(videoduration)) + "------------------------"
            title = parser.get_title_on_homepage(videoduration[i])
            title32 = parser.split_title(str(title))
            print title32
            url = htmlscraper.parse_href(videoduration[i])
            print url
            videoduration1 = parser.get_video_duration_on_categories(videoduration[i])
            thumbnail = parser.get_thumbnail(videoduration[i])
            print thumbnail
            duration = parser.split_video_duration_on_categories(str(videoduration1))
            print duration
            video_id = parser.parse_video_id(videoduration[i])
            iframe_object = parser.create_video_iframe(str(video_id[0]))
            print iframe_object
            videoPage = br.scrap_website(htmlscraper.parse_href(videoduration[i]))
            soup = BeautifulSoup(videoPage)
            print parser.parse_tags(htmlscraper.parse_all_href(soup))
        except:
            pass

def scraping_categories(br, htmlscraper, parser, output):
    parser = parsers.parser_xvideos.XvideosParser(output)
    categories = parser.parse_categories(output)
    for j in range(len(parser.parse_categories(output))):
        try:
            print "Parsing " + categories[j] + " ... "
            xvideoscategory = br.scrap_website(categories[j])
            soup = BeautifulSoup(xvideoscategory)
            categoryScrapedContent = parser.get_video_td_from_categories(soup)
            for j in range(len(categoryScrapedContent)):
                print "---------------------" + str(j) + " from " + str(len(categoryScrapedContent)) + "------------------------"
                title = parser.get_title_on_homepage(categoryScrapedContent[j])
                title32 = parser.split_title(str(title))
                print title32
                url = htmlscraper.parse_href(categoryScrapedContent[j])
                print url
                videoduration1 = parser.get_video_duration_on_categories(categoryScrapedContent[j])
                thumbnail = parser.get_thumbnail(categoryScrapedContent[j])
                print thumbnail
                duration = parser.split_video_duration_on_categories(str(videoduration1))
                print duration
                video_id = parser.parse_video_id(categoryScrapedContent[j])
                iframe_object = parser.create_video_iframe(str(video_id[0]))
                print iframe_object
                videoPage = br.scrap_website(htmlscraper.parse_href(categoryScrapedContent[j]))
                soup = BeautifulSoup(videoPage)
                print parser.parse_tags(htmlscraper.parse_all_href(soup))
        except:
            pass


br = common.startBrowser.BotBrowser()
xvideoshomepage = br.scrap_website('http://www.xvideos.com/')
htmlscraper = common.html_tag_parser.HtmlTagParser(xvideoshomepage)
parser = parsers.parser_xvideos.XvideosParser(xvideoshomepage)

scraping_homepage(br, htmlscraper, parser, xvideoshomepage)
scraping_categories(br, htmlscraper, parser, xvideoshomepage)

print "Scraping finished"