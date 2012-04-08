import functions.parser_xvideos
import functions.startBrowser

br = functions.startBrowser.BotBrowser()
output = br.scrap_website('http://www.xvideos.com')

parser = functions.parser_xvideos.XvideosParser()
results = parser.parse_xvideos_videos(output);
results = parser.parse_xvideos_categories(output);


print parser.parse_xvideos_video_id(output);

 < iframe src = "http://flashservice.xvideos.com/embedframe/1927535" frameborder = 0 width = 510 height = 400 scrolling = no ></ iframe >