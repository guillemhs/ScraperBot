import parsers.parser_xvideos
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup
import common.postCreator
import sys
import os
from common.dataHandler import DataHandler

class xVideosScraper():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")
        self.dataHandler = DataHandler()

    def scrape_videos(self, br, htmlscraper, parser, wpPost, videoUrls):
        postList = wpPost.get_posts(1500)
        for i in range(len(videoUrls)):
            try:
                print "---------------------" + str(i) + " from " + str(len(videoUrls)) + "------------------------"
                title = htmlscraper.convert_underscore_into_space(parser.split_url(videoUrls[i]))
                print "title: " + htmlscraper.uppercase_first_letter_from_string(title)
                if (self.dataHandler.is_this_item_on_the_list(title, postList)):
                    print "Content already posted"
                else:
                    print "url " + videoUrls[i]
                    title_as_categories = htmlscraper.convert_hypen_into_space(title)
                    categories = htmlscraper.convert_string_into_categories(title_as_categories)
                    print "title convert to categories: " + str(categories)
                    soup = BeautifulSoup(br.scrap_website(videoUrls[i]))
                    print "video page scraped "
                    duration = parser.get_video_duration(soup)
                    duration_for_snippets = parser.prepare_duration_for_snippets(duration)
                    print "duration for snippets: " + duration_for_snippets
                    duration = duration + "min"
                    print "duration " + duration
                    thumbnail = parser.get_thumbnail(soup)
                    print "thumbnail: " + thumbnail
                    video_id = parser.get_video_id(videoUrls[i])
                    iframe_object = parser.create_video_iframe(video_id)
                    print "iframe: " + iframe_object
                    embedurl = htmlscraper.parse_src_from_video_iframe(iframe_object)
                    print "embedurl " + embedurl
                    print "Wordpress post creator starting ..."
                    wpPost.createPost(title, thumbnail, iframe_object, duration, duration_for_snippets, categories, embedurl)
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
        print "xVideos scraper bot is starting ..."
        br = common.startBrowser.BotBrowser()
        homepage = br.scrap_website('http://www.xvideos.com/')
        htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
        parser = parsers.parser_xvideos.XvideosParser(homepage)
        wpPost = common.postCreator.PostCreator()
        scraper = xVideosScraper()
        soup = BeautifulSoup(homepage)
        totalUrlsVideos = parser.getUrlsFromVideos(soup)
        totalUrlsCategories = parser.getUrlsFromCategories(soup)
        totalUrlsVideos = list(set(totalUrlsVideos))
        totalUrlsCategories = list(set(totalUrlsCategories))
        scraper.scrape_videos(br, htmlscraper, parser, wpPost, totalUrlsVideos)
        scraper.scrape_from_category(br, htmlscraper, parser, wpPost, totalUrlsCategories, scraper)
        print "Scraping finished"

xVideosScraper().main()