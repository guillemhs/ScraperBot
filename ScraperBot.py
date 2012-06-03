import sys
from bots.youpornScraper import YouPornScraper

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
                youporn.main()


ScraperBot().main()