import parsers.parser_youporn
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup
import common.postCreator
import sys
import os
from common.dataHandler import DataHandler

class YouPornScraper():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")
        self.dataHandler = DataHandler()

    def scrape_videos(self, br, htmlscraper, parser, wpPost, videoUrls):
        postList = wpPost.get_posts(1000)
        for i in range(len(videoUrls)):
            try:
                print "---------------------" + str(i) + " from " + str(len(videoUrls)) + "------------------------"
                title = htmlscraper.convert_hypen_into_space(parser.split_url(videoUrls[i]))
                print "title: " + htmlscraper.uppercase_first_letter_from_string(title)
                if (self.dataHandler.is_this_item_on_the_list(title, postList)):
                    print "Content already posted"
                else:
                    print "Video scraping started ..."
                    tags = htmlscraper.convert_title_to_categories(str(title))
                    soup = BeautifulSoup(br.scrap_website(videoUrls[i]))
                    soup.prettify()
                    thumbnail = parser.get_thumbnail(soup)
                    print "thumbnail: " + thumbnail
                    paraVideo = parser.parse_video_id(videoUrls[i])
                    iframe = parser.create_video_iframe(paraVideo[0], paraVideo[1])
                    print "iframe: " + iframe
                    video_duration = parser.get_duration(soup)
                    print "video duration: " + video_duration
                    embedurl = htmlscraper.parse_src_from_video_iframe(iframe)
                    print "embedurl " + embedurl
                    duration_for_snippets = parser.prepare_duration_for_snippets(video_duration)
                    print "duration for snippets: " + duration_for_snippets
                    print "Wordpress post creator starting ..."
                    wpPost.createPost(title, thumbnail, iframe, video_duration, duration_for_snippets, tags, embedurl)
                    print "Scraped video [OK]"
            except:
                pass

    def scrape_from_category(self, br, htmlscraper, parser, wpPost, categoryUrls, scraper):
        print "scraping videos from categories"
        for i in range(len(categoryUrls)):
            soup = BeautifulSoup(br.scrap_website(categoryUrls[i]))
            totalUrlsVideos = parser.getUrlsFromVideos(soup)
            totalUrlsVideos = list(set(totalUrlsVideos))
            scraper.scrape_videos(br, htmlscraper, parser, wpPost, totalUrlsVideos)

    def main(self):
        print "Youporn scraper bot is starting ..."
        br = common.startBrowser.BotBrowser()
        homepage = br.scrap_website('http://www.youporn.com/')
        htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
        parser = parsers.parser_youporn.YoupornParser(homepage)
        wpPost = common.postCreator.PostCreator()
        scraper = YouPornScraper()
        soup = BeautifulSoup(homepage)
        totalUrlsVideos = parser.getUrlsFromVideos(soup)
        totalUrlsCategories = parser.getUrlsFromCategories(soup)
        totalUrlsVideos = list(set(totalUrlsVideos))
        totalUrlsCategories = list(set(totalUrlsCategories))
        scraper.scrape_videos(br, htmlscraper, parser, wpPost, totalUrlsVideos)
        scraper.scrape_from_category(br, htmlscraper, parser, wpPost, totalUrlsCategories, scraper)
        print "Youporn scraper bot is finishing ..."

YouPornScraper().main()