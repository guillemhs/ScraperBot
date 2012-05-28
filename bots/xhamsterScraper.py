import parsers.parser_xhamster
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup
import common.postCreator
import sys
import os
from common.dataHandler import DataHandler

class xHamsterScraper():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")
        self.dataHandler = DataHandler()

    def scrape_videos(self, br, htmlscraper, parser, wpPost, videoUrls, soupFromPage):
        postList = wpPost.get_posts(10)
        for i in range(len(videoUrls)):
            try:
                print "---------------------" + str(i) + " from " + str(len(videoUrls)) + "------------------------"
                title = htmlscraper.convert_underscore_into_space(parser.split_url(videoUrls[i]))
                print "title: " + htmlscraper.uppercase_first_letter_from_string(title)
                if (self.dataHandler.is_this_item_on_the_list(title, postList)):
                    print "Content already posted"
                else:
                    print "Video scraping started ..."
                    tags = htmlscraper.convert_title_to_categories(str(title))
                    thumbnail = parser.get_thumbnail(soupFromPage)
                    print "thumbnail: " + thumbnail
                    paraVideo = parser.parse_video_id(videoUrls[i])
                    iframe = parser.create_video_iframe(paraVideo)
                    print "iframe: " + iframe
                    soupFromVideoPage = BeautifulSoup(br.scrap_website(str(videoUrls[i])))
                    video_duration = parser.get_duration(soupFromVideoPage)
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
            soupFromCategory = BeautifulSoup(br.scrap_website(categoryUrls[i]))
            totalUrlsVideos = parser.getUrlsFromVideos(soupFromCategory)
            totalUrlsVideos = list(set(totalUrlsVideos))
            scraper.scrape_videos(br, htmlscraper, parser, wpPost, totalUrlsVideos, soupFromCategory)

    def main(self):
        print "xhamster scraper bot is starting ..."
        br = common.startBrowser.BotBrowser()
        homepage = br.scrap_website('http://www.xhamster.com')
        htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
        parser = parsers.parser_xhamster.xHamsterParser(homepage)
        wpPost = common.postCreator.PostCreator()
        scraper = xHamsterScraper()
        soup = BeautifulSoup(homepage)
        totalUrlsVideos = parser.getUrlsFromVideos(soup)
        totalUrlsVideos = list(set(totalUrlsVideos))
        totalUrlsCategories = parser.getUrlsFromCategories(soup)
        totalUrlsCategories = list(set(totalUrlsCategories))
        scraper.scrape_videos(br, htmlscraper, parser, wpPost, totalUrlsVideos, soup)
        scraper.scrape_from_category(br, htmlscraper, parser, wpPost, totalUrlsCategories, scraper)
        print "xhamster scraper bot is finishing ..."

xHamsterScraper().main()