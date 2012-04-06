from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class MySpider( CrawlSpider ):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = ( 
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule( SgmlLinkExtractor( allow = ( '' ) ), callback = 'parse_item' ),
    )

    def parse_item( self, response ):
        self.log( 'Hi, this is an item page! %s' % response.url )
