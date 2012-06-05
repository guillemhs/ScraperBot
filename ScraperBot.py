import sys
from bots.youpornScraper import YouPornScraper
from bots.xvideosScraper import xVideosScraper
from bots.xhamsterScraper import xHamsterScraper

class ScraperBot():
    def get_the_args(self):
        args = sys.argv
        args.remove(args[0])
        return args

    def main(self):
        args = self.get_the_args()
        for arg in args:
            if arg == 'youporn':
                youporn = YouPornScraper()
                youporn.__init__()
                youporn.main()
            if arg == 'xvideos':
                xvideos = xVideosScraper()
                xvideos.__init__()
                xvideos.main()
            if arg == 'xhamster':
                xhamster = xHamsterScraper()
                xhamster.__init__()
                xhamster.main()


ScraperBot().main()