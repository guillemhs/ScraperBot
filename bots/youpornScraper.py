import parsers.parser_youporn
import common.startBrowser, common.html_tag_parser
from BeautifulSoup import BeautifulSoup
import common.postCreator
import sys
import os

class YouPornScraper():

    def __init__(self):
        homeDirectory = os.getenv("HOME")
        sys.path.append(r"" + homeDirectory + "/ScraperBot" + "")

    def scrape_videos(self, br, htmlscraper, parser, wpPost, output, videoUrls):
        print "scraping videos"
        for i in range(len(videoUrls)):
            try:
                print "---------------------" + str(i) + " from " + str(len(videoUrls)) + "------------------------"
                title = htmlscraper.convert_hypen_into_space(parser.split_url(htmlscraper.parse_href(reu[i])))
                print " Scraping started ..."
                print "title: " + htmlscraper.uppercase_first_letter_from_string(title)
                title_as_categories = htmlscraper.convert_title_to_categories(str(title))
                print "title convert to categories: " + str(title_as_categories)
                url = "http://www.youporn.com" + htmlscraper.parse_href(reu[i])
                print "url: " + url
                print "url objects: " + htmlscraper.convert_hypen_into_space(parser.split_url(url))
                strIntoCategories = htmlscraper.convert_hypen_into_space(parser.split_url(url))
                print htmlscraper.convert_string_into_categories(strIntoCategories)
                thumbnail = parser.get_thumbnail(reu[i])
                print "thumbnail: " + thumbnail
                paraVideo = parser.parse_video_id(url)
                iframe = parser.create_video_iframe(paraVideo[0], paraVideo[1])
                print "iframe: " + iframe
                soup = BeautifulSoup(br.scrap_website(url))
                cat_and_tags = parser.get_tags_and_categories(soup)
                cats = BeautifulSoup(str(cat_and_tags[0]))
                cat = parser.extract_categories(htmlscraper.parse_all_href(cats))
                print "categories: " + cat
                tags = BeautifulSoup(str(cat_and_tags[1]))
                tag = parser.extract_categories(htmlscraper.parse_all_href(tags))
                print "tags: " + tag
                video_duration = parser.get_duration(soup)
                print "video duration: " + video_duration
                print "Wordpress post creator starting ..."
                wpPost.createPost(title, thumbnail, iframe, video_duration, cat, tag)
                print "Scraped video [OK]"
            except:
                pass


    def scraping_homepage(self, br, htmlscraper, parser, wpPost, output):
        print "scraping homepage"
        reu = parser.get_video_box()
        for i in range(len(reu)):
            try:
                print "---------------------" + str(i) + " from " + str(len(reu)) + "------------------------"

                title = htmlscraper.convert_hypen_into_space(parser.split_url(htmlscraper.parse_href(reu[i])))
                print " Scraping started ..."
                print "title: " + htmlscraper.uppercase_first_letter_from_string(title)
                title_as_categories = htmlscraper.convert_title_to_categories(str(title))
                print "title convert to categories: " + str(title_as_categories)
                url = "http://www.youporn.com" + htmlscraper.parse_href(reu[i])
                print "url: " + url
                print "url objects: " + htmlscraper.convert_hypen_into_space(parser.split_url(url))
                strIntoCategories = htmlscraper.convert_hypen_into_space(parser.split_url(url))
                print htmlscraper.convert_string_into_categories(strIntoCategories)
                thumbnail = parser.get_thumbnail(reu[i])
                print "thumbnail: " + thumbnail
                paraVideo = parser.parse_video_id(url)
                iframe = parser.create_video_iframe(paraVideo[0], paraVideo[1])
                print "iframe: " + iframe
                soup = BeautifulSoup(br.scrap_website(url))
                cat_and_tags = parser.get_tags_and_categories(soup)
                cats = BeautifulSoup(str(cat_and_tags[0]))
                cat = parser.extract_categories(htmlscraper.parse_all_href(cats))
                print "categories: " + cat
                tags = BeautifulSoup(str(cat_and_tags[1]))
                tag = parser.extract_categories(htmlscraper.parse_all_href(tags))
                print "tags: " + tag
                video_duration = parser.get_duration(soup)
                print "video duration: " + video_duration
                print "Wordpress post creator starting ..."
                wpPost.createPost(title, thumbnail, iframe, video_duration, cat, tag)
                print "Scraped video [OK]"
            except:
                pass


    def main(self):
        print "Youporn scraper bot is starting ..."
        br = common.startBrowser.BotBrowser()
        homepage = br.scrap_website('http://www.youporn.com/')
        htmlscraper = common.html_tag_parser.HtmlTagParser(homepage)
        parser = parsers.parser_youporn.YoupornParser(homepage)
        wpPost = common.postCreator.PostCreator()
        scraper = YouPornScraper()
        soup = BeautifulSoup(homepage)
        totalUrlsVideos = parser.getUrlsFromVideos(soup, htmlscraper)
        totalUrlsCategories = parser.getUrlsFromCategories(soup, htmlscraper)
        print totalUrlsVideos
        print totalUrlsCategories
        #scraper.scraping_homepage(br, htmlscraper, parser, wpPost, homepage)
        #print "Scraping finished"

YouPornScraper().main()