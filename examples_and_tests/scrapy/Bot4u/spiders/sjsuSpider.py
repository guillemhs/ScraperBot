from scrapy import log # This module is useful for printing out debug information
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class SjsuSpider( CrawlSpider ):

	name = 'sjsu'
	allowed_domains = ['sjsu.edu']
	start_urls = ['http://cs.sjsu.edu/']
	# allow=() is used to match all links
	rules = [Rule( SgmlLinkExtractor( allow = () ), follow = True ),
	         Rule( SgmlLinkExtractor( allow = () ) )]

	def parse_item( self, response ):
		self.log( 'Hi, this is an item page! %s' % response.url )
		open( "someLog.txt", 'wb' ).write( response.body )
