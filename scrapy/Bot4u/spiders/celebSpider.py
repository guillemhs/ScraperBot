from itemsCelebs import CelebItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

class CelebSpider(CrawlSpider): 
    name = "astro" 
    allowed_domains = ["www.astro.com"] 
    start_urls = [ 
"http://www.astro.com/astro-databank/Special:AllPages/Aadland%2C_Beverly" 
    ] 
    rules = ( 
        Rule(SgmlLinkExtractor(allow=('Beverly', ), deny=('Special', ))), 
    ) 
    
    def parse_item( self, response ):
        hxs = HtmlXPathSelector( response )
        extractedStr = hxs.select( "//table[@class='infoboxtoccolours']//table/tbody/tr/td[1]/text()" ).extract()
        item = CelebItem()
        item['name'] = extractedStr
        print item
        return item