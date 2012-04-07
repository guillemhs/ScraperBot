from beautiful_soup import BeautifulSoup as bs
from scrapy.spider import BaseSpider

class MininovaImprovedCrawler( BaseSpider ):
    name = 'mininovaImproved'
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org']

    def parse( self, response ):
        soup = bs( response.body )

        for link in soup.find_all( 'a' ):
            print( link.get( 'href' ) )
