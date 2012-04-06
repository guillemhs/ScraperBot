import itemsMininova
import os
import hashlib

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

PATH = os.path.abspath( os.path.join( __file__, '../../outMininova/' ) )

class MininovaCrawlSpider( CrawlSpider ):

    name = 'mininova.org'
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org/today']
    rules = [Rule( SgmlLinkExtractor( allow = ['/tor/\d+'] ) )]

    def parse( self, response ):
        x = HtmlXPathSelector( response )
        torrent = itemsMininova.TorrentItem()
        torrent['urlsite'] = response.url
        torrent['name'] = x.select( "//h1/text()" ).extract()
        torrent['description'] = x.select( "//div[@id='description']" ).extract()
        torrent['size'] = x.select( "//div[@id='info-left']/p[2]/text()[2]" ).extract()
        sha1_response = hashlib.sha1( response.url ).hexdigest()
        folder = PATH + '/' + sha1_response
        if not os.path.exists( folder ):
            os.makedirs( folder )
        with open( folder + '/index.html', 'w+' ) as file_obj:
            file_obj.write( response.body )
        return torrent

