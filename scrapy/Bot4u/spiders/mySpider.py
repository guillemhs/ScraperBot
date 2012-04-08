from scrapy import log # This module is useful for printing out debug information
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request.form import FormRequest

class MySpider( CrawlSpider ):
    name = 'myspider'
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org']

    rules = ( 
        Rule( SgmlLinkExtractor( allow = r'-\w+.html$' ),
             callback = 'parse_item', follow = True ),
    )

    def init_request( self ):
        self.log( "This function is called before crawling starts." )
        return self.login()

    def login( self, response ):
        """Generate a login request."""
        return FormRequest.from_response( response,
                    formdata = {'name': 'herman', 'password': 'password'},
                    callback = self.check_login_response )

    def check_login_response( self, response ):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "Hi Herman" in response.body:
            self.log( "Successfully logged in. Let's start crawling!" )
            # Now the crawling can begin..
            self.initialized()
        else:
            self.log( "Bad times :(" )
            # Something went wrong, we couldn't log in, so nothing happens.