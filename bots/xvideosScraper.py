import parsers.parser_xvideos
import common.startBrowser, common.html_tag_parser

br = common.startBrowser.BotBrowser()
htmlscraper = common.html_tag_parser.HtmlTagParser()
output = br.scrap_website('http://www.xvideos.com/')

parser = parsers.parser_xvideos.XvideosParser(output)

videoduration = parser.get_video_td()

title = parser.get_title_on_homepage(videoduration[0])
print title
videoduration1 = parser.get_video_duration(videoduration[0])
print videoduration1

video_id = parser.parse_video_id(videoduration[0])
print video_id

iframe_object = parser.create_video_iframe(video_id[0])
print iframe_object