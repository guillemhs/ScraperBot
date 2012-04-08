import functions.parser
import functions.startBrowser

br = functions.startBrowser.BotBrowser()
output = br.scrap_website('http://www.xvideos.com')

# Try and process the page.
# The class should have been defined first, remember.
myparser = functions.parser.Parser()
