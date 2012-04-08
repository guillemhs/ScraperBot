from parser import Parser
from startBrowser import BotBrowser

br = BotBrowser()
output = br.scrap_website('http://www.xvideos.com')

print output

# Try and process the page.
# The class should have been defined first, remember.
myparser = Parser()
print myparser.get_hyperlinks()